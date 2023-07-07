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
    $("#btn_compare").change(function () {
        var checkboxcount = $(".check_select:checked").length;

        if (checkboxcount == 0){
            $("#btn_compare").prop("disabled", true);
        }
    })

})

