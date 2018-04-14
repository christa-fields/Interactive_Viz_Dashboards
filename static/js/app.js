$.get( "http://127.0.0.1:5000/names", function( data ) {
    for(var i = 0; i < data.length; i++) {
        $('#selDataset').append($('<option/>', {value: data[i], text: data[i]}))
   }
    console.log(data);
});

$("#selDataset").on('change', function(e) { 
    $.get("http://127.0.0.1:5000/metadata/" + $(this).val(), function( data ){
    console.log(data)
    })  
    console.log($(this).val()) 
    
    buildPie($(this).val());

    buildPlot($(this).val());

    buildTable($(this).val());
})


// function buildTextbox(){

// }

// buildTextbox();

// Turorial for loop vs map method for an array
// var sample = [1,2,3,4,5]
// var sample_new =  []

// for (var i = 0; i < sample.length; i++) {
//     sample_new[i] = sample[i] * 2
// }; 

// console.log(sample_new)


// var sample_1 = sample.map(function(item){
//    return item * 2
// }) 

// console.log(sample_1)


function buildPie(sample_id){
    /* data route */
    var url = "http://127.0.0.1:5000/samples/" + sample_id;
    var url_2= "http://127.0.0.1:5000/otu";
    Plotly.d3.json(url, function(error, response){
        Plotly.d3.json(url_2, function(error, otuData){
            console.log(response);

            var labels = response[0]['otu_ids'].map(function(item) {            
                return otuData[item] });

                console.log(labels)
                console.log(response[0]['sample_values'])

            var layout = {height: 400, width: 500}

            var bubble_layout = {
                margin:{ t: 0},
                hovermode: "closest",
                xaxis:{title: "OTU IDs"}
            }

            var pie_data = [
                {
                    values: response[0]['sample_values'].slice(0, 10),                 
                    labels: response[0]['otu_ids'].slice(0, 10),                 
                    hovertext: labels.slice(0, 10),                 
                    hoverinfo: 'hovertext',                 
                    type: 'pie'
                }];
            
            var bubble_data = [{                
                x: response[0]['otu_ids'],
                y: response[0]['sample_values'],
                text: labels,
                mode:"markers",
                marker:{
                size:response[0]['sample_values'],
                color: response[0]['otu_ids'],
                colorscale:"Earth"
                }
            }]

                console.log(pie_data)
                console.log(bubble_data)

            var pie_element = $('#pie')
            var bubble_element = $('#bubble')
    
            Plotly.newPlot("pie", pie_data, layout)   
            Plotly.newPlot("bubble", bubble_data, bubble_layout)   
        })
    });
};

function buildTable(sample_id){
    /* data route */
    var url = "http://127.0.0.1:5000/metadata/" + sample_id;

        Plotly.d3.json(url, function(error, response){
            console.log(response);

            console.log(table_data)

            var table_layout = {height: 400, width: 200}

            var table_data = [{
                values: response[0]
            }]

            var table_element = $('#table')

            Plotly.newPlot("table", table_data, table_layout)
        });
}