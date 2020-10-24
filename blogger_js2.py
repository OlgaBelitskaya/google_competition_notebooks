# -*- coding: utf-8 -*-
"""blogger_js2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iSic065FfMG3jWSQdoKzQ-bHqrBJpTfZ
"""

from IPython.display import HTML
HTML("""
<script src="https://code.highcharts.com/highcharts.js"></script>
<script src="https://code.highcharts.com/highcharts-3d.js"></script>
<script src="https://code.highcharts.com/modules/accessibility.js"></script>
<figure class="highcharts-figure">
<div id="hich" style="width:500px; height:500px;"></div></figure><script>
function randi(min,max) {return Math.floor(Math.random()*(max-min+1))+min;};
var d=.005,l=5,n=3,a=randi(11,19),b=randi(24,64);
function ar(k,a,b) {return Array(1280).fill(k).map((k,t)=>
    [k*(Math.cos(d*t)+Math.sin(a*d*t)/2-Math.cos(b*d*t)/6),
     k*(Math.sin(d*t)+Math.cos(a*d*t)/2-Math.sin(b*d*t)/6),k]);};
Highcharts.setOptions({
    colors:Highcharts.getOptions().colors.map(function (color) {return {
radialGradient:{cx:.4,cy:.3,r:.2},
stops:[[0,color],
       [1,Highcharts.color(color).brighten(-0.2).get('rgb')]]};})});
var series=[];
for (var i=1; i<n+1; i++){
    series.push({name:i,colorByPoint:true,
                 accessibility:{exposeAsGroupOnly:true},
                 marker:{radius:1},data:ar(i,a,b)})};
var chart=new Highcharts.Chart({
    chart:{renderTo:'hich',margin:100,type:'scatter3d',
    animation:false,
    options3d:{enabled:true,alpha:20,beta:20,depth:250,
               viewDistance:5,fitToPlot:false,
               frame:{bottom:{size:1,color:'rgba(0,0,0,0.2)'},
                      back:{size:1,color:'rgba(0,0,0,0.25)'},
                      side:{ size:1,color:'rgba(0,0,0,0.3)'}}} },
  title:{text:'Scatter 3D with rotation in space'},
  plotOptions:{scatter:{width:l,height:l,depth:l}},
  yAxis:{min:-l,max:l,title:null},
  xAxis:{min:-l,max:l,gridLineWidth:1},
  zAxis:{min:0,max:l,showFirstLabel:false},
  legend:{enabled:false},series:series});
(function(H){function dragStart(eStart){
    eStart=chart.pointer.normalize(eStart);
    var posX=eStart.chartX,posY=eStart.chartY,
        alpha=chart.options.chart.options3d.alpha,
        beta=chart.options.chart.options3d.beta,
        sensitivity=3,handlers=[];
    function drag(e){
      e=chart.pointer.normalize(e);
      chart.update({chart:{
          options3d:{alpha:alpha+(e.chartY-posY)/sensitivity,
                     beta:beta+(posX-e.chartX)/sensitivity}}},
                    undefined,undefined,false);}
    function unbindAll(){handlers.forEach(function(unbind){
        if (unbind){unbind();}});
        handlers.length=0;}
    handlers.push(H.addEvent(document,'mousemove', drag));
    handlers.push(H.addEvent(document,'touchmove', drag));
    handlers.push(H.addEvent(document,'mouseup',unbindAll));
    handlers.push(H.addEvent(document,'touchend',unbindAll));}
  H.addEvent(chart.container,'mousedown',dragStart);
  H.addEvent(chart.container,'touchstart',dragStart);
}(Highcharts));</script>""")

from IPython.display import HTML
HTML("""<style>
@import url('https://fonts.googleapis.com/css?family=Ewert&effect=3d');
</style>
</script><script src="https://d3js.org/d3.v5.js"></script>
<script>
const url='https://raw.githubusercontent.com/holtzy/'+
          'D3-graph-gallery/master/DATA/data_correlogram.csv';
const url2='https://olgabelitskaya.github.io/beethoven.csv';
const st=`x,y,z
1.418,-1.494,-2.541
1.259,-1.563,-2.426
1.236,-1.686,-2.711
1.409,-1.614,-2.865
1.225,-1.777,-2.939`;
const data=d3.csvParse(st,d3.autoType);
var x=[],y=[],z=[];
for (var i=0; i<data.length; i++){
    x.push(data[i]['x']); y.push(data[i]['y']); z.push(data[i]['z'])};
var doc=document.getElementById('p1');
doc.innerHTML+=[x[0],y[0],z[0]];
</script>
<p id='p1' class='font-effect-3d' 
style='font-family:Ewert; font-size:25px; color:#ff0033;'>
Array elements: <br/></p>""")

from IPython.display import HTML
HTML("""
<script src="https://www.gstatic.com/charts/loader.js">
</script><script type="text/javascript">
google.charts.load('current',{'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
  var data=new google.visualization.DataTable();
  data.addColumn('number','id'); data.addColumn('number','x');
  data.addColumn('number','y'); data.addColumn('number','z');
  data.addRows([[1,1.418,-1.494,-2.541],[2,1.259,-1.563,-2.426],
                [3,1.236,-1.686,-2.711],[4,1.409,-1.614,-2.865],
                [5,1.225,-1.777,-2.939]]);
  var options={'title':'Coordinates',
               'width':500,'height':500};
  var doc=document.getElementById('chart_div');
  var chart=new google.visualization.ScatterChart(doc);
  chart.draw(data, options);}
</script><div id="chart_div"></div>""")

from IPython.display import HTML
HTML("""
<script src='https://www.gstatic.com/charts/loader.js'>
</script></script><script src='https://d3js.org/d3.v5.js'></script>
<script type='text/javascript'>
google.charts.load('current',{'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
const st=`x,y,z
1.418,-1.494,-2.541
1.259,-1.563,-2.426
1.236,-1.686,-2.711
1.409,-1.614,-2.865
1.225,-1.777,-2.939`;
const xyz=d3.csvParse(st,d3.autoType);
var x=[],y=[],z=[];
for (var i=0; i<5; i++){
  x.push(xyz[i]['x']); 
  y.push(xyz[i]['y']); 
  z.push(xyz[i]['z'])};
function drawChart() {
  var data=new google.visualization.DataTable();
  data.addColumn('number','id'); data.addColumn('number','v1');
  data.addColumn('number','v2'); data.addColumn('number','v3');
  for (var i=0; i<5; i++){
      data.addRow([i+1,x[i],y[i],z[i]]);};
  var options={'title':'Charts with DataTables',
               'width':500,'height':500};
  var doc=document.getElementById('chdiv02');
  var chart=new google.visualization.AreaChart(doc);
  chart.draw(data,options);}
</script><div id='chdiv02'></div>""")

from IPython.display import HTML
HTML("""
<script src='https://d3js.org/d3.v4.min.js'>
</script><svg id='chsvg01' style='background-color:slategray;'></svg><script>
var url='https://olgabelitskaya.github.io/castle.csv'
d3.csv(url,function(data) {
var n=data.length,m=35,margin={top:m,right:m,bottom:m,left:m},
    width=500-margin.left-margin.right,
    height=300-margin.top-margin.bottom; 
var xScale=d3.scaleLinear().domain([-1000,1000]).range([0,width]); 
var yScale=d3.scaleLinear().domain([0,1000]).range([height,0]);
function make_x_gridlines() {return d3.axisBottom(xScale).ticks(11)}; 
function make_y_gridlines() {return d3.axisLeft(yScale).ticks(11)};
var pointColor=d3.scaleSequential().domain([0,n])
                 .interpolator(d3.interpolateCool);       
var svg=d3.select('#chsvg01').attr('width',width+margin.left+margin.right)
          .attr('height',height+margin.top+margin.bottom)
          .append('g').attr('transform',
                            'translate('+margin.left+','+margin.top+')');
svg.append('g').attr('class','xaxis1').call(d3.axisBottom(xScale).tickSize(.5))
               .attr('transform','translate(0,'+height+')'); 
svg.append('g').attr('class','yaxis1').call(d3.axisLeft(yScale).tickSize(.5));    
svg.append('g').attr('class','grid1').attr('transform','translate(0,'+height+')')
               .call(make_x_gridlines().tickSize(-height).tickFormat(''));
svg.append('g').attr('class','grid1').call(make_y_gridlines()
               .tickSize(-width).tickFormat(''));
svg.selectAll('.point').data(data).enter()
   .append('circle').attr('class','point')
   .attr('fill',function(d,i){return pointColor(i)}).attr('r',2)
   .attr('stroke','#ffffff').attr('stroke-width','.3')
   .attr('cx',function(d) {return xScale(d.x)})
   .attr('cy',function(d) {return yScale(d.z)}); });
</script>""")