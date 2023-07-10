$(document).ready(function() {
    $(".check_select").change(function () {
        var checkboxcount = $(".check_select:checked").length;

        if (checkboxcount == 2){
             $(':checkbox:not(:checked)').prop('disabled', true);
        }
        else{
            $(':checkbox:not(:checked)').prop('disabled', false);
        }
    })
})


$("#btn_compare").on("click",function(){
    console.log("Button clicked")
    var selectedValues = $('input[name="xmlFile"]:checked').map(function(){
        return $(this).attr('fileName');
    }).get();
    console.log("Before AJAX")
    $.ajax({
        url: "/compare_xml/",
        type: "POST",
        headers: { "X-CSRFToken": csrf_token },
        data:{
            "file1":selectedValues[0],
            "file2":selectedValues[1]
        },
        success: function(data) {

            console.log("Inside Success")
            // console.log("Data =",data.diff)
            $("#comparexml").modal("show")

            const xmlString = data.diff;
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlString, "text/xml");

            // Retrieve the employee elements
            const employees = xmlDoc.getElementsByTagName("employee");

            // Create a container element to hold the XML content
            const container = document.getElementById("employeesContainer");

            // Iterate over each employee and add them to the container
            for (let i = 0; i < employees.length; i++) {
                const employee = employees[i];

                // Create a new <pre> element for the XML content
                const pre = document.createElement("pre");

                // Format the XML content and set it as the <pre> element's text
                pre.textContent = formatXml(new XMLSerializer().serializeToString(employee));

                // Apply the "added-data" class if data was added
                if (employee.getAttribute("diff:insert")) {
                    pre.classList.add("added-data");
                }
                // Append the <pre> element to the container
                container.appendChild(pre);
            }
        },
        error: function(data) {
            console.log("Inside Error")
        }
    });
})

function formatXml(xml) {
    let formattedXml = "";
    const reg = /(>)(<)(\/*)/g;
    xml = xml.replace(reg, "$1\n$2$3");
    const pad = 2;

    xml.split("\n").forEach(function(node) {
      let indent = 0;
      if (node.match(/.+<\/\w[^>]*>$/)) {
        indent = 0;
      } else if (node.match(/^<\/\w/)) {
        if (indent !== 0) {
          indent -= pad;
        }
      } else if (node.match(/^<\w[^>]*[^\/]>.*$/)) {
        indent += pad;
      } else {
        indent = 0;
      }

      let padding = "";
      for (let i = 0; i < indent; i++) {
        padding += " ";
      }

      formattedXml += padding + node + "\n";
    });

    return formattedXml;
  }



// $("#btn_compare").on("click",function() {
//     $("#comparexml").modal("show")
// })

