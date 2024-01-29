const App = {
    data () {
        return {
            // counter: 0,
            currentPage: 0,
            addPlace: 0,
            addRoute :1,
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

            editingRouteList : [

            ],

            selectedOnRouteEditMapSight : '',

            editRouteName :'',
            editRouteDescription: '',

            notes : ['task 1', 'task 2'],

            selectedTagsExactlyYes :[],
            avaliableTagsExactlyYes :["Volga", "Ne Volga", "Home"],
            selectedTagsExactlyNo :[],
            avaliableTagsExactlyNo :["Ne Volga", "Volga", "no Homo"]
            
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
            if (this.addPlace) {
            this.startMap();

            }
            if (this.addRoute) {
                this.startCreatingNewRouteMap();
            }
            
        }
        if (this.currentPage == 4) {
            
        }
    },

    methods : {
        swapTwoPlacesInEditingRouteList(id1, id2) {
            if (id1 >= 0 && id2 >= 0 && id1 < this.editingRouteList.length && id2 < this.editingRouteList.length) {

                // let swap = editingRouteList[editingRouteList.find((element) => element.id === id1)]
                // editingRouteList[editingRouteList.find((element) => element.id === id1)] = editingRouteList[editingRouteList.find((element) => element.id === id2)]
                // editingRouteList[editingRouteList.find((element) => element.id === id2)] = swap
                let swap = this.editingRouteList[id1];
                this.editingRouteList[id1] = this.editingRouteList[id2];
                this.editingRouteList[id2] = swap;
            }
        },

        tryToSaveRoute () {
            console.log(this.editRouteName);
            console.log(this.editRouteDescription);
            fetch("/create/route", 
                {
                    method: "POST",
                    body: JSON.stringify({ 
                        newRouteList : this.editingRouteList,
                        // name : 'name'
                        newRouteName : this.editRouteName,
                        newRouteDescription : this.editRouteDescription
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
                    this.deleteEditing();
            });
                
        },
        deleteEditing() {
            this.editingRouteList = [];
            this.editRouteName = '';
            this.editRouteDescription = '';
        },

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
            
            function updateSightsPoints(listd) {
                // window.map.getLayers().getArray()
                // .filter(layer => layer.get('name') === 'Markers')
                // .forEach(layer => map.removeLayer(layer));

                markers.clearMarkers();
                
                console.log(listd.length);
                for(var i = 0; i < listd.length; i++)
                { 
                    (function(i){
                        var lonLat = new OpenLayers.LonLat(listd[i].lon, listd[i].lat).transform( fromProjection, toProjection);
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
                        // console.log('json[sights] = ', json['sights']);
                        // console.log('json[sights] = ',  JSON.parse(json)['sights']);

                        updateSightsPoints(JSON.parse(json)['sights']);
                      
                    });
                }

                getSightsPoins(map);
            
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
                        this.selectedOnRouteEditMapSight = json
                });
                
        },

        logout () {
            localStorage.clear();
            // window.location.pathname = 'login'; 
            window.location.reload();
        }
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
