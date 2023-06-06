const { spawn } = require('child_process');
const express = require('express');
const router = express.Router();
//const { e_obj } = require('./config');

const {
  //エラー処理ミドルウェアの読み込み
  CheckReqParam,
  ValidateRequestBody,
} = require('./err');
const { ErrorMessageController } = require('./ErrController');

router.post('/', (req, res, next) => {
  if (!res.writableFinished) ValidateRequestBody(req.body, '0001', next);
  if (!res.writableFinished) CheckReqParam(req.body, '0002', next);

  if (!res.writableFinished) {
    const message = req.body.message;
    console.log(message);
    let dataToSend;

    //ファイルをコマンドで実行するのと同じ
    const python = spawn('python3', ['./main.py', message], {
      env: { PYTHONIOENCODING: 'cp65001' }, //ここで文字コードの指定
    });

    python.stdout.on('data', function (data) {
      console.log('――――稼働中――――');
      dataToSend = data.toString();
    });
    python.stderr.on('data', (data) => {
      console.log(`stderr: ${data}`);
    });
    python.on('exit', (code) => {
      console.log(`=========結果=========\n${dataToSend}`);
      res.json({ data: dataToSend });
    });
  }
});

function errorHandler(err, req, res, next) {
  console.error(err.stack);
  const errRes = {
    error: {
      code: '',
      message: '',
    },
  };
  //エラーをクライアントに返す
  if (err.e_code == undefined) {
    //拾いきれなかった想定外のエラーが発生した場合
    errRes.error.code = '500_UnhandledException';
    errRes.error.message = '想定外のエラーが発生しました';
    return res.status(500).json(errRes);
  }
  const e = ErrorMessageController(err.e_code);
  errRes.error.code = err.e_code;
  errRes.error.message = e.e_msg;
  console.log(errRes);
  return res.status(err.statusCode).json(errRes);
}

//router.use(logErrors); //実際の実行
router.use(errorHandler);
module.exports = router;
