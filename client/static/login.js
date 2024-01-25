

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
        // inputChangeHandler (event) {
        //     console.log("inputChangeHandlers : ", event.target.value);
        //     this.inputValue = event.target.value;
        // },
        // addNewNote() {
        //     this.notes.push(this.inputValue);
        //     this.inputValue = "";
        // } ,

        // inputKeyPress(event) {
        //     console.log(event.key);
        //     if (event.key === "Enter") {
        //         this.addNewNote();
        //     }
            
        // },
        // removeNote(idx, event) {
        //     console.log("renove", idx, event);
        //     this.notes.splice(idx, 1)
        // },
        // switchPage(idx) {

        // }
        
    }
}


// const app = Vue.createApp(App)
// app.mount("#app")

// or

Vue.createApp(App).mount("#app")
