function validform() {

        var a = document.forms["my-form"]["firstName"].value;
        var b = document.forms["my-form"]["email-address"].value;
        var c = document.forms["my-form"]["phone_number"].value;
        var d = document.forms["my-form"]["address"].value;
        var e = document.forms["my-form"]["password"].value;
        var f = document.forms["my-form"]["confirm-password"].value;

        if (a==null || a=="")
        {
            alert("Please Enter Your First Name");
            return false;
        }else if (b==null || b=="")
        {
            alert("Please Enter Your Email Address");
            return false;
        }else if (c==null || c=="")
        {
            alert("Please Enter Your phone number");
            return false;
        }else if (d==null || d=="")
        {
            alert("Please Enter Your Permanent Address");
            return false;
        }else if (e==null || e=="")
        {
            alert("Please Enter password");
            return false;
        }else if (f==null || f=="")
        {
            alert("Please Enter confirm password");
            return false;
        }

    }