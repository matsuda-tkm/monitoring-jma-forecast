function getJSON() {
  var now = new Date();
  var date = Utilities.formatDate(now, "GMT+9", "yyyyMMddHHmmss");
  var weather_all = {};
  var areaCodeList = ["011000","012000","016000","013000","014100","015000","017000","020000","050000","030000","040000","060000","070000","080000","090000","100000","110000","120000","130000","140000","200000","190000","220000","230000","210000","240000","150000","160000","170000","180000","250000","260000","270000","280000","290000","300000","330000","340000","320000","310000","360000","370000","380000","390000","350000","400000","440000","420000","410000","430000","450000","460100","471000","472000","473000","474000"];

  for (var j=0; j<areaCodeList.length; j++) {
    console.log(areaCodeList[j]);
    const weatherUrl = 'https://www.jma.go.jp/bosai/forecast/data/forecast/' + areaCodeList[j] + '.json';
    var weatherj = UrlFetchApp.fetch(weatherUrl);
    var weather = JSON.parse(weatherj);
    weather_all[areaCodeList[j]] = weather;
  }

  // JSONを保存
  var folderId = "xxxxxxxxxxxxxxxxxxxxxx";
  var weatherString = JSON.stringify(weather_all);
  var fileName = date + ".json";
  var folder = DriveApp.getFolderById(folderId);
  var file = folder.createFile(fileName, weatherString);
  Logger.log("JSON file created and saved: " + file.getUrl());
}