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
            
            
            var lat            = 59.9275;
            var lon            = 30.3346;
            var zoom           = 12;

            var fromProjection = new OpenLayers.Projection("EPSG:4326");   // Transform from WGS 1984
            var toProjection   = new OpenLayers.Projection("EPSG:900913"); // to Spherical Mercator Projection
            var position       = new OpenLayers.LonLat(lon, lat).transform( fromProjection, toProjection);

            map = new OpenLayers.Map("demoMap");
            var mapnik         = new OpenLayers.Layer.OSM();
            map.addLayer(mapnik);

            // var markers = new OpenLayers.Layer.Markers( "Markers" );
            // map.addLayer(markers);
            // markers.addMarker(new OpenLayers.Marker(position));
            var markers = new OpenLayers.Layer.Markers("Markers");

            listd = [//30.3648853,59.9306793
                {Longitude : 30.3648853,
                    Latitude : 59.9306793   ,
                    id : 0,
                }, //30.4102421,59.9239807
                {Longitude : 30.4102421,
                    Latitude : 59.9239807,
                    id : 1,
                },
            ]
            console.log(listd.length);
            for(var i = 0; i < listd.length; i++)
            { 
                (function(i){
                     var lonLat = new OpenLayers.LonLat(listd[i].Longitude, listd[i].Latitude).transform( fromProjection, toProjection);
                    console.log(lonLat);
                    
                    //  var title = listd[i].Title;
                    //  var iconPath = listd[i].IconPath;
                    //  var size = new OpenLayers.Size(15, 22);
                    //  var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
            
                    //  var icon = new OpenLayers.Icon(iconPath, size, offset);
                     var marker = new OpenLayers.Marker(lonLat); //, icon.clone()
                    marker.id = listd[i].id
                    // console.log(marker);
                     markers.addMarker(marker);
                    //  console.log(markers);
                    
                    marker.events.register("click", marker, function(e){
                    //     // popup = new OpenLayers.Popup.FramedCloud("chicken",
                    //     //     marker.lonlat,
                    //     //     new OpenLayers.Size(200, 200),
                    //     //     title,
                    //     //     null, false );
                    //     //   map.addPopup(popup);
                        console.log(marker.id);
                     });
                })(i);
             } 
             map.addLayer(markers);
            //  console.log(map);


            map.setCenter(position, zoom);
            console.log("getExtent = ", map.getExtent().transform(toProjection, fromProjection));
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
