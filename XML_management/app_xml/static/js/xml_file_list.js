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
        },
        error: function(data) {
            console.log("Inside Error")
        }
    });
})


$("#btn_compare").on("click",function() {
    $("#comparexml").modal("show")
})

