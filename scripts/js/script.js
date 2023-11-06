function teste(){
    var username = $("#username").val()
    var password = $("#password").val()

    console.log(username, password)
    $.ajax({
        url: "http://127.0.0.1:5000\login",
        METHOD: "POST",
        contentType:'aplication/json',
        data: {
            username:username,
            password:password
        },
        success: function(data){
            console.log(data)
        }
    })
}