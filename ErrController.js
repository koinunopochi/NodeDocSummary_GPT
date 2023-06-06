const {e_obj} = require("./config.json");
/**
 * 独自のエラーコードを受け取り、エラーデータを返す
 * @param {string} e_code
 * @returns {object} err_obj
 */
exports.ErrorMessageController = function (err_code) {
  const errIndex = e_obj.find((err) => err.code == err_code).index;
  return e_obj[errIndex];
};
