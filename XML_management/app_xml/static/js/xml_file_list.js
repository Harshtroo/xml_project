$("#btn_compare").on("click", function () {
  $("#comparexml").modal("show")
})

$(".btn-close").on("click",function() {
   location.reload();
   $("#comparexml").modal("hide")
})

$(document).ready(function () {
  $(".check_select").change(function () {
    var checkboxcount = $(".check_select:checked").length;

    if (checkboxcount == 0){
        $("#btn_compare").prop('disabled', true)
    }


    if (checkboxcount == 2) {
      $(':checkbox:not(:checked)').prop('disabled', true);
    }
    else {
      $(':checkbox:not(:checked)').prop('disabled', false);
    }
  })
})

//
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
        console.log("file1====", data.file1_data)
        file1 = data.file1_data
        file2 = data.file2_data
        $("#comparexml").modal("show")

        var table1_val = document.getElementById('file1_table').getElementsByTagName('tbody')[0]
        file1.forEach((file_data,index) => {
               table1_val.innerHTML += `<tr>
                                    <td>${index}</td>
                                    <td>${file_data.id}</td>
                                    <td>${file_data.firstname}</td>
                                    <td>${file_data.lastname}</td>
                                    <td>${file_data.title}</td>
                                    <td>${file_data.division}</td>
                                    <td>${file_data.building}</td>
                                    <td>${file_data.room}</td>
                                    </tr>`
               })

        var table2_val = document.getElementById('file2_table').getElementsByTagName('tbody')[0]

        file2.forEach((file_data,index) => {
               i=1
               table2_val.innerHTML += `<tr>
                                    <td>${index}</td>
                                    <td>${file_data.id}</td>
                                    <td>${file_data.firstname}</td>
                                    <td>${file_data.lastname}</td>
                                    <td>${file_data.title}</td>
                                    <td>${file_data.division}</td>
                                    <td>${file_data.building}</td>
                                    <td>${file_data.room}</td>
                                    </tr>`

               })

        const firstTable = document.querySelectorAll("#file1_table td")
        const secondTable = document.querySelectorAll("#file2_table td");

        for (let i=0; i< firstTable.length; i++){
                console.log("ftable==============",firstTable[i].textContent)
            if (firstTable[i].textContent !== secondTable[i].textContent) {
                console.log("++++++++++++++++++++++=",firstTable[i].textContent !== secondTable[i].textContent)
                firstTable[i].classList.add('redbg');// here do what you need to when not equal
                console.log("???????????????????///",firstTable[i].classList.add('redbg'))
          }
        }



        },

    error: function (data) {
      console.log("Inside Error")
        }
    })
})

