const App = {
    data () {
        return {
            // counter: 0,
            currentPage: 0,
            addPlace: 1,
            addRoute :0,
            placeholderString : "введите название заметок",
            title: "список заметок",
            inputValue: "",
            newsListLeft : [
                {
                    type : "event",
                    id : 0,
                    title : "Smth new and timelimited",
                    description : "have time to visit!",
                    images : [""]
                },
                {
                    type : "place",
                    id : 0,
                    title : "New interesting place",
                    description : "Some Description",
                    images : [""]
                },
                {
                    type : "route",
                    id : 0,
                    title : "Interesting route",
                    description : "New interesting route",
                    images : [""]
                },
                {
                    type : "topic",
                    id : 0,
                    title : "Topic",
                    description : "Long read",
                    images : [""]
                }
            ],

            newsListRight : [
                {
                    type : "event",
                    id : 0,
                    title : "Smth new and timelimited",
                    description : "have time to visit!",
                    images : [""]
                },
                {
                    type : "place",
                    id : 0,
                    title : "New interesting place",
                    description : "Some Description",
                    images : [""]
                },
                {
                    type : "route",
                    id : 0,
                    title : "Interesting route",
                    description : "New interesting route",
                    images : [""]
                },
                {
                    type : "topic",
                    id : 0,
                    title : "Topic",
                    description : "Long read",
                    images : [""]
                }
            ],

            notes : ['task 1', 'task 2'],
            
        }
    },

    updated(){
        if (this.currentPage == 0) {
            // document.getElementById("news").style.color="#0D99FF";
        }
        if (this.currentPage == 1) {

        }
        if (this.currentPage == 2) {
            console.log("map updated");
            this.startMap();
        }
        if (this.currentPage == 3) {
            this.startMap();
        }
        if (this.currentPage == 4) {
            
        }
    },

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
        startMap() {
            console.log("map called", document.getElementById("demoMap"));
            
            // console.log("current page = " this.currentPage);
            // while(document.getElementById("demoMap") === null) {
            //     console.log("rendering");
            // }
            // map = new OpenLayers.Map("demoMap");
            // map.addLayer(new OpenLayers.Layer.OSM());
            // map.zoomToMaxExtent();
            var lat            = 47.35387;
            var lon            = 8.43609;
            var zoom           = 18;

            var fromProjection = new OpenLayers.Projection("EPSG:4326");   // Transform from WGS 1984
            var toProjection   = new OpenLayers.Projection("EPSG:900913"); // to Spherical Mercator Projection
            var position       = new OpenLayers.LonLat(lon, lat).transform( fromProjection, toProjection);

            map = new OpenLayers.Map("demoMap");
            var mapnik         = new OpenLayers.Layer.OSM();
            map.addLayer(mapnik);

            var markers = new OpenLayers.Layer.Markers( "Markers" );
            map.addLayer(markers);
            markers.addMarker(new OpenLayers.Marker(position));

            map.setCenter(position, zoom);
        },

        logout () {
            localStorage.clear();
            // window.location.pathname = 'login'; 
            window.location.reload();
        }
    }
}


// const app = Vue.createApp(App)
// app.mount("#app")

// or

Vue.createApp(App).mount("#app")
