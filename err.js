//const { e_obj } = require('./config');
const { ErrorMessageController } = require('./ErrController');
/**
 * bodyの要素の値チェックし、必要な変数名が含まれているかチェック 400 throw
 * @param {*} body req.body
 * @param {*} next
 */
exports.ValidateRequestBody = function (body, code, next) {
  const { message } = body;
  if (message == undefined) {
    throwError(code, next);
  }
};
/**
 * req.bodyに含まれる必須パラメータの値チェック 400 throw
 * @param {*} body req.body
 * @param {*} next
 */
exports.CheckReqParam = function (body, code, next) {
  const prams = [body.message];
  for (const param of prams) {
    if (param == '') {
      throwError(code, next);
    }
  }
};
/**
 * errコードを受けとり、configからエラーメッセージを取得し、throwする
 * @param {string} code
 * @param {*} next
 */
const throwError = (code, next) => {
  const e = ErrorMessageController(code);
  const err_m = e.throw_msg;
  const status = e.status;
  next(new CustomError(err_m, status, code));
};

/**
 * Errorをthrowし、nextに渡す
 */
class CustomError extends Error {
  constructor(message, statusCode, e_code) {
    super(message);
    this.statusCode = statusCode;
    this.e_code = e_code;
  }
}
