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
        // console.log("file1====", data.file1_content, "file2======", data.file2_content)
        $("#comparexml").modal("show")
        $("#file1_data").text(data.file1_content)
        $("#file2_data").text(data.file2_content)

        var parser = new DOMParser();
        var xmlDoc1 = parser.parseFromString(data.file1_content, "text/xml");
        var xmlDoc2 = parser.parseFromString(data.file2_content, "text/xml");

        var differences = compareXMLNodes(xmlDoc1.documentElement, xmlDoc2.documentElement);
        console.log("?????????????????????????",differences)
        highlightChanges(differences);
    
},

    error: function (data) {
      console.log("Inside Error")
        }
  });
})




function compareXMLNodes(node1, node2) {
    // Compare the nodes and return the differences
    // You can implement your own comparison logic here
    // For simplicity, this example assumes the XML structure is similar
    // and only compares the node names and values
  
    var differences = [];
  
    if (node1.nodeName !== node2.nodeName) {
      differences.push({
        type: "deleted",
        node: node1
      });
      differences.push({
        type: "added",
        node: node2
      });
    } else if (node1.nodeValue !== node2.nodeValue) {
      differences.push({
        type: "modified",
        node: node1
      });
      differences.push({
        type: "modified",
        node: node2
      });
    }
    return differences;
}

function highlightChanges(differences) {
    // Modify the HTML representation of the XML files to highlight changes
    // This example assumes the XML files are displayed in <pre> elements
    // with IDs "file1_data" and "file2_data"
  
    var file1Data = $("#file1_data");
    var file2Data = $("#file2_data");
  
    differences.forEach(function (difference) {
      var node = difference.node;
  
      if (difference.type === "added") {
        $(node).css("color", "green");
    } else if (difference.type === "deleted") {
        $(node).css("color", "red");
      }
    });
  } 