//
// app.js
// @author: Brian
//

function tableInfo(table){
  var tableName = document.getElementById(table);
  var name = table.trim();
  var name2 = name.split("&#x27;")
  console.log("tableInfo: ", name2);
  tableName.value = name;
  return name;
}
