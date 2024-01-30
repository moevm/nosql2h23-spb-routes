

const App = {
    data () {
        return {
            // counter: 0,
            pageType : {SignIn : "SignIn", 
                RecoveryAccess : "RecoveryAccess", 
                RecoverySccessWithCode : "RecoverySccessWithCode", 
                ForgotPassword : "ForgotPassword", 
                SignUp : "SignUp"}
,

            currentPage: "SignIn",
            
            email : "",
            password : "",
            
            firstName : "",
            lastName: "",
            address: "",
            phone: "",
            // : "",

            repeatPassword : "",

           

            passwordsAreEq : false,
            
        }
    },

    // updated(){
    //     if (this.currentPage == 0) {
    //         // document.getElementById("news").style.color="#0D99FF";
    //     }
    //     if (this.currentPage == 1) {

    //     }
    //     if (this.currentPage == 2) {
    //         console.log("map updated");
    //         this.startMap();
    //     }
    //     if (this.currentPage == 3) {
    //         this.startMap();
    //     }
    //     if (this.currentPage == 4) {
            
    //     }
    // },

    methods : {
        
        tryToLogin () {
            // console.log(this.email, this.email);
            // return;
            let form = new FormData()
            form.append("username", this.email)
            form.append("password", this.password)

            const formData = new URLSearchParams(form)


            fetch("/auth/token", {
            method: "POST",
            body: formData,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            }).then((response) => {window.location.href = response.url; response.json(); json}).then((json) => {localStorage.access_token = json.access_token; 
                
                // window.location.href = '/';
                // fetch('/redirect_to_main_page', {
                //     method: 'GET',
                //     redirect: 'follow',
                //     headers: {
                //       Authorization: 'Bearer '+ localStorage.access_token ,  
                //     }
                //   }).then((response) => {window.location.href = response.url;});//window.location.replace(response));// console.log(response));
            });
        },

        tryToCreateNewUser () {


            fetch("/auth/create/user", 
            {
            method: "POST",
            body: JSON.stringify({ 
                email: this.email,
                password: this.password,
                firstName: this.firstName,
                lastName: this.lastName,
                phone: this.phone,
                address: this.address,
            }),
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
                // Authorization: 'Bearer '+ localStorage.access_token ,
            }
            }
            ).then((response) => response.json()).then((json) => {//localStorage.access_token = json.access_token; 
                console.log(json);
                if (json.isUserCreated) {
                    // console.log("success");
                    this.tryToLogin();
                } else {
                    console.log('fail');
                }
                // window.location.href = '/';
                // fetch('/redirect_to_main_page', {
                //     method: 'GET',
                //     redirect: 'follow',
                //     headers: {
                //       Authorization: 'Bearer '+ localStorage.access_token ,  
                //     }
                //   }).then((response) => {window.location.href = response.url;});//window.location.replace(response));// console.log(response));
            });

        }


        
    }
}


// const app = Vue.createApp(App)
// app.mount("#app")

// or

Vue.createApp(App).mount("#app")
