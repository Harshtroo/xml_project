$("#btn_compare").on("click", function () {
  $("#comparexml").modal("show")
})

$(document).ready(function () {
  $(".check_select").change(function () {
    var checkboxcount = $(".check_select:checked").length;

    if (checkboxcount == 2) {
      $(':checkbox:not(:checked)').prop('disabled', true);
    }
    else {
      $(':checkbox:not(:checked)').prop('disabled', false);
    }
  })
})


$("#btn_compare").on("click", function () {
  console.log("Button clicked")
  var selectedValues = $('input[name="xmlFile"]:checked').map(function () {
    return $(this).attr('fileName');
  }).get();
  console.log("Before AJAX")
  $.ajax({
    url: "/compare_xml/",
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    data: {
      "file1": selectedValues[0],
      "file2": selectedValues[1]
    },
    success: function (data) {
      console.log("Inside Success")
      console.log("file1====", data.file1_content, "file2======", data.file2_content)
      $("#comparexml").modal("show")
      $("#file1_data").text(data.file1_content)
      $("#file2_data").text(data.file2_content)

//      outputDataOld = ""
//      outputDataNew = ""
//
//      var oldList = " "
//      var newList = " "
//
//      firstIdValues = data.file1_content
//      secondIdValues = data.file2_content
//      for (let i = 1; i < firstIdValues.length; i++) {
//        if (firstIdValues[i] == secondIdValues[i]) {
//          if (firstIdValues[i] == secondIdValues[i]) {
//            outputDataOld += `${firstIdValues[i]}`
//            outputDataNew += `${secondIdValues[i]}`
//          }
//          else {
//            if (firstIdValues[i].toLowerCase() == secondIdValues[i].toLowerCase()) {
//              console.log("string match but cases does not match")
//              for (j = 0; j < firstIdValues[i].length; j++) {
//                if (firstIdValues[i][j] == secondIdValues[i][j]) {
//                  oldList += firstIdValues[i][j]
//                  newList += secondIdValues[i][j]
//                }
//                else {
//                  oldList += `${firstIdValues[i][j]}`
//                  newList += `${secondIdValues[i][j]}`
//                }
//              }
//              outputDataOld += oldList
//              outputDataNew += newList
//              oldList = " "
//              newList = " "
//            }
//            else {
//              outputDataOld += `${firstIdValues[i]}`
//              outputDataNew += `${secondIdValues[i]}`
//            }
//          }
//        }
//        else {
//          outputDataOld += `${firstIdValues[i]}`
//          outputDataNew += `${secondIdValues[i]}`
//        }
//      }
//      $("#file1_data").append(outputDataOld);
//      $("#file2_data").append(outputDataNew);
//

    },
    error: function (data) {
      console.log("Inside Error")
    }
  });
})

//function formatXml(xml) {
//    let formattedXml = "";
//    const reg = /(>)(<)(\/*)/g;
//    xml = xml.replace(reg, "$1\n$2$3");
//    const pad = 2;
//
//    xml.split("\n").forEach(function(node) {
//      let indent = 0;
//      if (node.match(/.+<\/\w[^>]*>$/)) {
//        indent = 0;
//      } else if (node.match(/^<\/\w/)) {
//        if (indent !== 0) {
//          indent -= pad;
//        }
//      } else if (node.match(/^<\w[^>]*[^\/]>.*$/)) {
//        indent += pad;
//      } else {
//        indent = 0;
//      }
//
//      let padding = "";
//      for (let i = 0; i < indent; i++) {
//        padding += " ";
//      }
//
//      formattedXml += padding + node + "\n";
//    });
//
//    return formattedXml;
//  }




