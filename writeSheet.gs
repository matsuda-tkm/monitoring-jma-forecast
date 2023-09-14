function writeJSON() {
  // スプレッドシートとの接続
  const SHEET_ID = "xxxxxxxxxxxxxxxxxxxxxx";
  const SHEET_NAME = "data";
  var spreadSheet = SpreadsheetApp.openById(SHEET_ID);
  var sheet = spreadSheet.getSheetByName(SHEET_NAME);

  // JSONを取得
  var areaCodeList = ["011000","012000","016000","013000","014100","015000","017000","020000","050000","030000","040000","060000","070000","080000","090000","100000","110000","120000","130000","140000","200000","190000","220000","230000","210000","240000","150000","160000","170000","180000","250000","260000","270000","280000","290000","300000","330000","340000","320000","310000","360000","370000","380000","390000","350000","400000","440000","420000","410000","430000","450000","460100","471000","472000","473000","474000"];

  for (var j=0; j<areaCodeList.length; j++) {
    console.log(areaCodeList[j]);
    const weatherUrl = 'https://www.jma.go.jp/bosai/forecast/data/forecast/' + areaCodeList[j] + '.json';
    var weatherj = UrlFetchApp.fetch(weatherUrl);
    var weather = JSON.parse(weatherj);

    // JSON解析
    var sub = weather[1]['timeSeries'];
    var reportDatetime = weather[1]['reportDatetime'];
    var dates = sub[0]['timeDefines'];
    console.log(reportDatetime);

    var df = [];
    for (var i=0; i<dates.length; i++) {
      var line = [];
      line.push(reportDatetime);
      line.push(areaCodeList[j]);
      line.push(dates[i]);
      line.push(sub[0]['areas'][0]['weatherCodes'][i]);
      line.push(sub[0]['areas'][0]['pops'][i]);
      line.push(sub[0]['areas'][0]['reliabilities'][i]);
      line.push(sub[1]['areas'][0]['tempsMin'][i]);
      line.push(sub[1]['areas'][0]['tempsMinUpper'][i]);
      line.push(sub[1]['areas'][0]['tempsMinLower'][i]);
      line.push(sub[1]['areas'][0]['tempsMax'][i]);
      line.push(sub[1]['areas'][0]['tempsMaxUpper'][i]);
      line.push(sub[1]['areas'][0]['tempsMaxLower'][i]);
      df.push(line);
    }
    sheet.getRange(sheet.getLastRow()+1, 1, df.length, line.length).setValues(df);
    Utilities.sleep(100);
  }
}