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
          row.innerHTML = `<tr class="yellowText">
            <td>${index}</td>
            <td >${file_data.id}</td>
            <td >${file_data.firstname}</td>
            <td >${file_data.lastname}</td>
            <td >${file_data.title}</td>
            <td >${file_data.division}</td>
            <td >${file_data.building}</td>
            <td >${file_data.room}</td>;
            </tr>`

          var isInsertion = insertions.some((insertion) => insertion.id === file_data.id);
          if (isInsertion) {
            row.style.backgroundColor = '#99ff99';
          } else {
            var isDeletion = deletions.some((deletion) => deletion.id === file_data.id);
            var isUpdate = updates.some((update) => update.id === file_data.id);
            if (isDeletion) {
              row.style.backgroundColor = 'red';
            } else if (isUpdate) {

              const updateKeys = Object.keys(updates).filter(key => !file1.hasOwnProperty(key));

              const file1Keys = Object.keys(file1).filter(key => !updates.hasOwnProperty(key));

              const file1Table = document.getElementById("file1_table");
              const file2Table = document.getElementById("file2_table");

              for (let i = 0; i < file2Table.rows.length; i++) {
                  const file1Row = file1Table.rows[i];
                  const file2Row = file2Table.rows[i];

                  for (let j = 0; j < file2Row.cells.length; j++) {
                    const file1Val = (file1Row) ? file1Row.cells[j].textContent : '';
                    const file2Val = file2Row.cells[j].textContent;

                    if (file1Val !== file2Val) {
                      file2Row.cells[j].style.backgroundColor = "yellow";
                    }
                  }
              }
            }
          }
        });
        },
    error: function (data) {
      console.log("Inside Error")
        }
    })
})

