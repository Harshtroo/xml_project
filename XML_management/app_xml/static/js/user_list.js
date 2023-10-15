$("#employeeadd").on("click",function(){
    console.log("hello")
    $("#staticBackdrop").modal("show")
})

$(".close_btn").on("click",function(){
    $("#staticBackdrop").modal("hide")
})

$(document).ready(function() {
    $("#addEmployeeForm").submit(function(e) {

        e.preventDefault();
        $.ajax({
            url: employeeAddURL,
            type: "POST",
            data: $(this).serialize(),
            success: function(data) {

                    window.location.href = employeeRedirectURL;
                    console.log("message======",data.message)
                    if(data.message){
                    setTimeout(function (){
                         $('.output').html("<p class='textsuccess'>" + data.message + "</p>");
                        },1000)
                        setTimeout(function(){
                            $('.output').remove();
                          }, 3000);
                    }
            },
            error: function(data) {
                var errorMessage = data.error;
                $("#errorMessage").text(errorMessage);
            }
        });
    });
});
