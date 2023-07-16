$("#btn_compare").on("click", function () {
  $("#comparexml").modal("show")
})

$(".btn-close").on("click",function() {
   location.reload();
   $("#comparexml").modal("hide")
})

$(document).ready(function () {
  $(".check_select").change(function () {
    var checkboxCount = $(".check_select:checked").length;

      if (checkboxCount <= 1) {
        $("#btn_compare").prop('disabled', true);
      } else {
        $("#btn_compare").prop('disabled', false);
      }

    if (checkboxCount == 2) {
      $(':checkbox:not(:checked)').prop('disabled', true);
    }
    else {
      $(':checkbox:not(:checked)').prop('disabled', false);
    }
  })
})

//
$("#btn_compare").on("click", function () {
  var selectedValues = $('input[name="xmlFile"]:checked').map(function () {
    return $(this).attr('fileName');
  }).get();
  $.ajax({
    url: "/compare_xml/",
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    data: {
      "file1": selectedValues[0],
      "file2": selectedValues[1]
    },
    success: function (data) {
        var insertions = data.insertions
        var updates = data.updates
        var deletions = data.deletions

        var file1 = data.file1_data;
        var file2 = data.file2_data;

        $("#comparexml").modal("show");

        var table1_val = document.getElementById('file1_table').getElementsByTagName('tbody')[0];
        file1.forEach((file_data, index) => {
          var row = table1_val.insertRow();
          row.innerHTML =`<tr>
            <td>${index}</td>
            <td>${file_data.id}</td>
            <td>${file_data.firstname}</td>
            <td>${file_data.lastname}</td>
            <td>${file_data.title}</td>
            <td>${file_data.division}</td>
            <td>${file_data.building}</td>
            <td>${file_data.room}</td>;
            </tr>`

          var isInsertion = insertions.some((insertion) => insertion.id === file_data.id);
          if (isInsertion) {
            row.style.backgroundColor = 'green';
          } else {
            var isDeletion = deletions.some((deletion) => deletion.id === file_data.id);
            var isUpdate = updates.some((update) => update.id === file_data.id);
            if (isDeletion) {
              row.style.backgroundColor = 'red';
            }
          }
        });

        var table2_val = document.getElementById('file2_table').getElementsByTagName('tbody')[0];
        file2.forEach((file_data, index) => {
          var row = table2_val.insertRow();
          row.innerHTML = `<tr>
            <td>${index}</td>
            <td>${file_data.id}</td>
            <td>${file_data.firstname}</td>
            <td>${file_data.lastname}</td>
            <td>${file_data.title}</td>
            <td>${file_data.division}</td>
            <td>${file_data.building}</td>
            <td>${file_data.room}</td>;
            </tr>`

          var isInsertion = insertions.some((insertion) => insertion.id === file_data.id);
          if (isInsertion) {
            row.style.backgroundColor = '#99ff99';
          } else {
            var isDeletion = deletions.some((deletion) => deletion.id === file_data.id);
            var isUpdate = updates.some((update) => update.id === file_data.id);
//            console.log("isupdaqte==================",updates)
            if (isDeletion) {
              row.style.backgroundColor = 'red';
            } else if (isUpdate) {
              // var cellIndex = -1
              // row.style.backgroundColor = '#e5e500';
              const updateKeys = Object.keys(updates).filter(key => !file1.hasOwnProperty(key));

              // Find keys in file1 object that are not in updates
              const file1Keys = Object.keys(file1).filter(key => !updates.hasOwnProperty(key));

              const differentValues = Object.entries(updates).reduce((result, [key, value]) => {
                if (file1.hasOwnProperty(key) && file1[key] !== value) {
                  result[key] = {
                    oldValue: file1[key],
                    newValue: value
                  };
                }
                return result;
              }, {});
              const table = document.getElementById("file2_table");
              const updatedValues = [];
              for (let i = 0; i < table.rows.length; i++) {
                const row = table.rows[i];
                const cellKey = row.cells[0].textContent; // Assuming the key is in the first cell
              
                if (differentValues.hasOwnProperty(cellKey)) {
                  const cellNewValue = row.cells[i]; // Assuming the new value is in the second cell
                  const newValue = cellNewValue.textContent;
              
                  updatedValues.push(newValue);
                  
                  cellNewValue.style.backgroundColor = "yellow";
                }
              }
              console.log("updated val================================",updatedValues)
            }
          }
        });
        },

    error: function (data) {
      console.log("Inside Error")
        }
    })
})

