const App = {
    data () {
        return {

            showedPlace : '',
            // code under must be deleted

            // counter: 0,
            currentPage: 0,
            addPlace: 0,
            addRoute :1,


            editingRouteList : [

            ],

            selectedOnRouteEditMapSight : '',

            editRouteName :'',
            editRouteDescription: '',


            
            showedRoute : '',

            showedRouteList : [],

            allUserRoutes: '',

        }
    },

    mounted() {
        this.startCreatingNewRouteMap();

     },

    updated(){
        if (this.currentPage == 0) {
            this.startCreatingNewRouteMap();

        }
        if (this.currentPage == 1) {
            if (this.allUserRoutes === '')
            this.getAllUserRoutes();
        }
        if (this.currentPage == 2) {
            
        }
        if (this.currentPage == 3) {
            
            
        }
        if (this.currentPage == 4) {
            
        }
    },

    methods : {
        getShowedRouteList() {
            // console.log(id);
            for (let i = 0; i < this.showedRoute["sightsSubsequenceIds"].length; i += 1){
                fetch("/get/sight/by/id", 
                    {
                        method: "POST",
                        body: JSON.stringify({ 
                            id : this.showedRoute["sightsSubsequenceIds"][i],
                        }),
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded"
                            // Authorization: 'Bearer '+ localStorage.access_token ,
                        }
                        }
                        ).then((response) => response.json()).then((json) => {
                        
                            // updateSightsPoints(JSON.parse(json)['sights']);
                            console.log(json);
                            console.log(this.showedRouteList)
                            this.showedRouteList.push(json);
                });
            }
              
        },

        getAllUserRoutes() {
            fetch("/get/all/routes", 
                {
                    method: "POST",
                    body: JSON.stringify({ 
                        placeholder : "None"
                        
                    }),
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                        // Authorization: 'Bearer '+ localStorage.access_token ,
                    }
                    }
                    ).then((response) => response.json()).then((json) => {
                        // console.log('json[sights] = ', json['sights']);
                        // console.log('json[sights] = ',  JSON.parse(json)['sights']);

                        // updateSightsPoints(JSON.parse(json)['sights']);
                        console.log(json);
                        this.allUserRoutes = json["userRoutes"];
                    // this.deleteEditing();
                    // this.tryToCancel()
            });
        },



        getSightById (id) {
            console.log(id);
            fetch("/get/sight/by/id", 
                {
                    method: "POST",
                    body: JSON.stringify({ 
                        id : id,
                    }),
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                        // Authorization: 'Bearer '+ localStorage.access_token ,
                    }
                    }
                    ).then((response) => response.json()).then((json) => {
                       
                        // updateSightsPoints(JSON.parse(json)['sights']);
                        console.log(json);
                        this.showedPlace = json
                });
                
        },


        startCreatingNewRouteMap() {
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

            
            var markers = new OpenLayers.Layer.Markers("Markers");
            
            updateSightsPoints = (listd) => {
               
                markers.clearMarkers();
                
                console.log(listd.length);
                for(var i = 0; i < listd.length; i++)
                { 
                    ((i)=> {
                        var lonLat = new OpenLayers.LonLat(listd[i].lon, listd[i].lat).transform( fromProjection, toProjection);
                        // console.log(lonLat);
                        
                        //  var title = listd[i].Title;
                        //  var iconPath = listd[i].IconPath;
                        //  var size = new OpenLayers.Size(15, 22);
                        //  var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
                
                        //  var icon = new OpenLayers.Icon(iconPath, size, offset);
                        var marker = new OpenLayers.Marker(lonLat); //, icon.clone()
                        marker.id = listd[i].id
                        markers.addMarker(marker);
                        
                        marker.events.register("click", marker, (e)=>{
                            this.getSightById(marker.id)
                        });
                    })(i);
                } 
                

            }
            //  console.log(map);
            map.addLayer(markers);

            

            map.setCenter(position, zoom);

            console.log(map);
            map.events.register("moveend", map, function() {
                getSightsPoins(map);
                
            });

            getSightsPoins = (map) => {
                let extent = map.getExtent().transform(toProjection, fromProjection);
                console.log("getExtent = ", extent);

                fetch("/get/dysplayable/points", 
                {
                    method: "POST",
                    body: JSON.stringify({ 
                        extent : extent
                    }),
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                        // Authorization: 'Bearer '+ localStorage.access_token ,
                    }
                    }
                    ).then((response) => response.json()).then((json) => {
                       
                        updateSightsPoints(JSON.parse(json)['sights']);
                      
                    });
                }

                getSightsPoins(map);
            
        },



        // code under must be deleted

        


        
    },
    // watch: {
    //     <>: function(){
    //       console.log('any of these variables changed');
    //     }
    // }
}


// const app = Vue.createApp(App)
// app.mount("#app")

// or
// Vue.prototype.window = window
// app.config.globalProperties.selectedOnRouteEditMapSight = 'selectedOnRouteEditMapSight';

Vue.createApp(App).mount("#app")
