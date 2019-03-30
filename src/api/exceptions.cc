// This file contains implementation of error APIs exposed in node.h

#include "env-inl.h"
#include "node.h"
#include "node_errors.h"
#include "util-inl.h"
#include "uv.h"
#include "v8.h"

#include <cstring>
#include <string>

namespace node {

using v8::Exception;
using v8::HandleScope;
using v8::Integer;
using v8::Isolate;
using v8::Local;
using v8::Message;
using v8::NewStringType;
using v8::Object;
using v8::String;
using v8::Value;

Local<Value> ErrnoException(Isolate* isolate,
                            int errorno,
                            const char* syscall,
                            const char* msg,
                            const char* path) {
  Environment* env = Environment::GetCurrent(isolate);
  CHECK_NOT_NULL(env);

  Local<Value> e;
  Local<String> estring = OneByteString(isolate, errors::errno_string(errorno));
  if (msg == nullptr || strlen(msg) == '0') {
    msg = strerror(errorno);
  }
  Local<String> message = OneByteString(isolate, msg);

  Local<String> cons =
      String::Concat(isolate, estring, FIXED_ONE_BYTE_STRING(isolate, ", "));
  cons = String::Concat(isolate, cons, message);

  Local<String> path_string;
  if (path != nullptr) {
    // FIXME(bnoordhuis) It's questionable to interpret the file path as UTF-8.
    path_string = String::NewFromUtf8(isolate, path, NewStringType::kNormal)
                      .ToLocalChecked();
  }

  if (path_string.IsEmpty() == false) {
    cons = String::Concat(isolate, cons, FIXED_ONE_BYTE_STRING(isolate, " '"));
    cons = String::Concat(isolate, cons, path_string);
    cons = String::Concat(isolate, cons, FIXED_ONE_BYTE_STRING(isolate, "'"));
  }
  e = Exception::Error(cons);

  Local<Object> obj = e.As<Object>();
  obj->Set(env->context(),
           env->errno_string(),
           Integer::New(isolate, errorno)).Check();
  obj->Set(env->context(), env->code_string(), estring).Check();

  if (path_string.IsEmpty() == false) {
    obj->Set(env->context(), env->path_string(), path_string).Check();
  }

  if (syscall != nullptr) {
    obj->Set(env->context(),
             env->syscall_string(),
             OneByteString(isolate, syscall)).Check();
  }

  return e;
}

static Local<String> StringFromPath(Isolate* isolate, const char* path) {
#ifdef _WIN32
  if (strncmp(path, R"(\\?\UNC\)", 8) == 0) {
    return String::Concat(
        isolate,
        FIXED_ONE_BYTE_STRING(isolate, "\\\\"),
        String::NewFromUtf8(isolate, path + 8, NewStringType::kNormal)
            .ToLocalChecked());
  } else if (strncmp(path, R"(\\?\)", 4) == 0) {
    return String::NewFromUtf8(isolate, path + 4, NewStringType::kNormal)
        .ToLocalChecked();
  }
#endif

  return String::NewFromUtf8(isolate, path, NewStringType::kNormal)
      .ToLocalChecked();
}


Local<Value> UVException(Isolate* isolate,
                         int errorno,
                         const char* syscall,
                         const char* msg,
                         const char* path,
                         const char* dest) {
  Environment* env = Environment::GetCurrent(isolate);
  CHECK_NOT_NULL(env);

  if (msg == nullptr || strlen(msg) == 0)
    msg = uv_strerror(errorno);

  Local<String> js_code = OneByteString(isolate, uv_err_name(errorno));
  Local<String> js_syscall = OneByteString(isolate, syscall);
  Local<String> js_path;
  Local<String> js_dest;

  Local<String> js_msg = js_code;
  js_msg =
      String::Concat(isolate, js_msg, FIXED_ONE_BYTE_STRING(isolate, ": "));
  js_msg = String::Concat(isolate, js_msg, OneByteString(isolate, msg));
  js_msg =
      String::Concat(isolate, js_msg, FIXED_ONE_BYTE_STRING(isolate, ", "));
  js_msg = String::Concat(isolate, js_msg, js_syscall);

  if (path != nullptr) {
    js_path = StringFromPath(isolate, path);

    js_msg =
        String::Concat(isolate, js_msg, FIXED_ONE_BYTE_STRING(isolate, " '"));
    js_msg = String::Concat(isolate, js_msg, js_path);
    js_msg =
        String::Concat(isolate, js_msg, FIXED_ONE_BYTE_STRING(isolate, "'"));
  }

  if (dest != nullptr) {
    js_dest = StringFromPath(isolate, dest);

    js_msg = String::Concat(
        isolate, js_msg, FIXED_ONE_BYTE_STRING(isolate, " -> '"));
    js_msg = String::Concat(isolate, js_msg, js_dest);
    js_msg =
        String::Concat(isolate, js_msg, FIXED_ONE_BYTE_STRING(isolate, "'"));
  }

  Local<Object> e =
    Exception::Error(js_msg)->ToObject(isolate->GetCurrentContext())
      .ToLocalChecked();

  e->Set(env->context(),
         env->errno_string(),
         Integer::New(isolate, errorno)).Check();
  e->Set(env->context(), env->code_string(), js_code).Check();
  e->Set(env->context(), env->syscall_string(), js_syscall).Check();
  if (!js_path.IsEmpty())
    e->Set(env->context(), env->path_string(), js_path).Check();
  if (!js_dest.IsEmpty())
    e->Set(env->context(), env->dest_string(), js_dest).Check();

  return e;
}

#ifdef _WIN32
// Does about the same as strerror(),
// but supports all windows error messages
static std::string winapi_strerror(const int errorno) {
  LPSTR msg = nullptr;
  // Because the 5th argument can be a simple IN parameter it's type is LPSTR,
  // but if FORMAT_MESSAGE_ALLOCATE_BUFFER, it's needs to be a double pointer.
  // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
  const auto msg_p = reinterpret_cast<LPSTR>(&msg);
  const DWORD flags = FORMAT_MESSAGE_ALLOCATE_BUFFER |
    FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS;
  DWORD i = FormatMessage(flags, nullptr, errorno, 0, msg_p, 0, nullptr);

  if (msg == nullptr || i <= 0) {
    // FormatMessage failed
    return "Unknown error";
  }
  // Remove trailing newlines
  for (; i >= 0 && (msg[i] == '\n' || msg[i] == '\r'); i--) {
    msg[i] = '\0';
  }
  const std::string ret{msg};
  LocalFree(msg);
  return ret;
}


Local<Value> WinapiErrnoException(Isolate* isolate,
                                  int errorno,
                                  const char* syscall,
                                  const char* msg,
                                  const char* path) {
  Environment* env = Environment::GetCurrent(isolate);
  CHECK_NOT_NULL(env);
  std::string message;
  if (msg != nullptr && strlen(msg)) {
    message = msg;
  } else {
    message = winapi_strerror(errorno);
  }
   

  Local<Object> obj;
  if (path != nullptr) {
    const std::string formatted = message + " '" + path + "'";
    const Local<String> msg_v8str = OneByteString(isolate, formatted.data());
    const auto path_v8str =
      String::NewFromUtf8(isolate, path, NewStringType::kNormal)
        .ToLocalChecked();
    obj = Exception::Error(msg_v8str).As<Object>();
    obj->Set(env->context(), env->path_string(), path_v8str).Check();
  } else {
    const Local<String> msg_v8str = OneByteString(isolate, message.data());
    obj = Exception::Error(msg_v8str).As<Object>();
  }

  obj->Set(env->context(), env->errno_string(), Integer::New(isolate, errorno))
      .Check();

  if (syscall != nullptr) {
    const auto syscall_str = OneByteString(isolate, syscall);
    obj->Set(env->context(), env->syscall_string(), syscall_str).Check();
  }

  return obj.As<Exception>();
}
#endif

void FatalException(Isolate* isolate, const v8::TryCatch& try_catch) {
  // If we try to print out a termination exception, we'd just get 'null',
  // so just crashing here with that information seems like a better idea,
  // and in particular it seems like we should handle terminations at the call
  // site for this function rather than by printing them out somewhere.
  CHECK(!try_catch.HasTerminated());

  HandleScope scope(isolate);
  if (!try_catch.IsVerbose()) {
    FatalException(isolate, try_catch.Exception(), try_catch.Message());
  }
}

}  // namespace node
