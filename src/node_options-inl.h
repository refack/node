#ifndef SRC_NODE_OPTIONS_INL_H_
#define SRC_NODE_OPTIONS_INL_H_

#if defined(NODE_WANT_INTERNALS) && NODE_WANT_INTERNALS

#include "node_options.h"
#include "util.h"
#include <initializer_list>
#include <memory>
#include <string>
#include <vector>

namespace node {

PerIsolateOptions* PerProcessOptions::get_per_isolate_options() {
  return per_isolate.get();
}

DebugOptions* EnvironmentOptions::get_debug_options() {
  return &debug_options_;
}

const DebugOptions& EnvironmentOptions::debug_options() const {
  return debug_options_;
}

EnvironmentOptions* PerIsolateOptions::get_per_env_options() {
  return per_env.get();
}

namespace options_parser {

template <typename Options>
void OptionsParser<Options>::AddOption(const std::string& name,
                                       const std::string& help_text,
                                       bool Options::* field,
                                       OptionEnvvarSettings env_setting) {
  options_.emplace(name,
                   OptionInfo{kBoolean,
                              std::make_shared<SimpleOptionField<bool>>(field),
                              env_setting,
                              help_text});
}

template <typename Options>
void OptionsParser<Options>::AddOption(const std::string& name,
                                       const std::string& help_text,
                                       uint64_t Options::* field,
                                       OptionEnvvarSettings env_setting) {
  options_.emplace(
      name,
      OptionInfo{kUInteger,
                 std::make_shared<SimpleOptionField<uint64_t>>(field),
                 env_setting,
                 help_text});
}

template <typename Options>
void OptionsParser<Options>::AddOption(const std::string& name,
                                       const std::string& help_text,
                                       int64_t Options::* field,
                                       OptionEnvvarSettings env_setting) {
  options_.emplace(
      name,
      OptionInfo{kInteger,
                 std::make_shared<SimpleOptionField<int64_t>>(field),
                 env_setting,
                 help_text});
}

template <typename Options>
void OptionsParser<Options>::AddOption(const std::string& name,
                                       const std::string& help_text,
                                       std::string Options::* field,
                                       OptionEnvvarSettings env_setting) {
  options_.emplace(
      name,
      OptionInfo{kString,
                 std::make_shared<SimpleOptionField<std::string>>(field),
                 env_setting,
                 help_text});
}

template <typename Options>
void OptionsParser<Options>::AddOption(
    const std::string& name,
    const std::string& help_text,
    std::vector<std::string> Options::* field,
    OptionEnvvarSettings env_setting) {
  options_.emplace(name, OptionInfo {
    kStringList,
    std::make_shared<SimpleOptionField<std::vector<std::string>>>(field),
    env_setting,
    help_text
  });
}

template <typename Options>
void OptionsParser<Options>::AddOption(const std::string& name,
                                       const std::string& help_text,
                                       HostPort Options::* field,
                                       OptionEnvvarSettings env_setting) {
  options_.emplace(
      name,
      OptionInfo{kHostPort,
                 std::make_shared<SimpleOptionField<HostPort>>(field),
                 env_setting,
                 help_text});
}

template <typename Options>
void OptionsParser<Options>::AddOption(const std::string& name,
                                       const std::string& help_text,
                                       NoOp no_op_tag,
                                       OptionEnvvarSettings env_setting) {
  options_.emplace(name, OptionInfo{kNoOp, nullptr, env_setting, help_text});
}

template <typename Options>
void OptionsParser<Options>::AddOption(const std::string& name,
                                       const std::string& help_text,
                                       V8Option v8_option_tag,
                                       OptionEnvvarSettings env_setting) {
  options_.emplace(name,
                   OptionInfo{kV8Option, nullptr, env_setting, help_text});
}

template <typename Options>
void OptionsParser<Options>::AddAlias(const std::string& from,
                                      const std::string& to) {
  aliases_[from] = { to };
}

template <typename Options>
void OptionsParser<Options>::AddAlias(const std::string& from,
                                      const std::vector<std::string>& to) {
  aliases_[from] = to;
}

template <typename Options>
void OptionsParser<Options>::AddAlias(
    const std::string& from,
    const std::initializer_list<std::string>& to) {
  AddAlias(from, std::vector<std::string>(to));
}

template <typename Options>
void OptionsParser<Options>::Implies(const std::string& from,
                                     const std::string& to) {
  auto it = options_.find(to);
  CHECK_NE(it, options_.end());
  CHECK_EQ(it->second.type, kBoolean);
  implications_.emplace(from, Implication {
    it->second.field, true
  });
}

template <typename Options>
void OptionsParser<Options>::ImpliesNot(const std::string& from,
                                        const std::string& to) {
  auto it = options_.find(to);
  CHECK_NE(it, options_.end());
  CHECK_EQ(it->second.type, kBoolean);
  implications_.emplace(from, Implication {
    it->second.field, false
  });
}

template <typename Options>
template <typename OriginalField, typename ChildOptions>
auto OptionsParser<Options>::Convert(
    std::shared_ptr<OriginalField> original,
    ChildOptions* (Options::* get_child)()) {
  // If we have a field on ChildOptions, and we want to access it from an
  // Options instance, we call get_child() on the original Options and then
  // access it, i.e. this class implements a kind of function chaining.
  struct AdaptedField : BaseOptionField {
    void* LookupImpl(Options* options) const override {
      return original->LookupImpl((options->*get_child)());
    }

    AdaptedField(
        std::shared_ptr<OriginalField> original,
        ChildOptions* (Options::* get_child)())
          : original(original), get_child(get_child) {}

    std::shared_ptr<OriginalField> original;
    ChildOptions* (Options::* get_child)();
  };

  return std::shared_ptr<BaseOptionField>(
      new AdaptedField(original, get_child));
}
template <typename Options>
template <typename ChildOptions>
auto OptionsParser<Options>::Convert(
    typename OptionsParser<ChildOptions>::OptionInfo original,
    ChildOptions* (Options::* get_child)()) {
  return OptionInfo{original.type,
                    Convert(original.field, get_child),
                    original.env_setting,
                    original.help_text};
}

template <typename Options>
template <typename ChildOptions>
auto OptionsParser<Options>::Convert(
    typename OptionsParser<ChildOptions>::Implication original,
    ChildOptions* (Options::* get_child)()) {
  return Implication {
    Convert(original.target_field, get_child),
    original.target_value
  };
}

template <typename Options>
template <typename ChildOptions>
void OptionsParser<Options>::Insert(
    const OptionsParser<ChildOptions>* child_options_parser,
    ChildOptions* (Options::* get_child)()) {
  aliases_.insert(child_options_parser->aliases_.begin(),
                  child_options_parser->aliases_.end());

  for (const auto& pair : child_options_parser->options_)
    options_.emplace(pair.first, Convert(pair.second, get_child));

  for (const auto& pair : child_options_parser->implications_)
    implications_.emplace(pair.first, Convert(pair.second, get_child));
}

inline std::string NotAllowedInEnvErr(const std::string& arg) {
  return arg + " is not allowed in NODE_OPTIONS";
}

inline std::string RequiresArgumentErr(const std::string& arg) {
  return arg + " requires an argument";
}

// We store some of the basic information around a single Parse call inside
// this struct, to separate storage of command line arguments and their
// handling. In particular, this makes it easier to introduce 'synthetic'
// arguments that get inserted by expanding option aliases.
struct ArgsInfo {
  // Generally, the idea here is that the first entry in `*underlying` stores
  // the "0th" argument (the program name), then `synthetic_args` are inserted,
  // followed by the remainder of `*underlying`.
  std::vector<std::string>* underlying;
  std::vector<std::string> synthetic_args;

  std::vector<std::string>* exec_args;

  ArgsInfo(std::vector<std::string>* args,
           std::vector<std::string>* exec_args)
    : underlying(args), exec_args(exec_args) {}

  size_t remaining() const {
    // -1 to account for the program name.
    return underlying->size() - 1 + synthetic_args.size();
  }

  bool empty() const { return remaining() == 0; }
  const std::string& program_name() const { return underlying->at(0); }

  std::string& first() {
    return synthetic_args.empty() ? underlying->at(1) : synthetic_args.front();
  }

  std::string pop_first() {
    std::string ret = std::move(first());
    if (synthetic_args.empty()) {
      // Only push arguments to `exec_args` that were also originally passed
      // on the command line (i.e. not generated through alias expansion).
      // '--' is a special case here since its purpose is to end `exec_argv`,
      // which is why we do not include it.
      if (exec_args != nullptr && ret != "--")
        exec_args->push_back(ret);
      underlying->erase(underlying->begin() + 1);
    } else {
      synthetic_args.erase(synthetic_args.begin());
    }
    return ret;
  }
};


}  // namespace options_parser
}  // namespace node

#endif  // defined(NODE_WANT_INTERNALS) && NODE_WANT_INTERNALS

#endif  // SRC_NODE_OPTIONS_INL_H_
