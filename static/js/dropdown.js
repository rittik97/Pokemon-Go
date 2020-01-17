console.log('dropwdown.js')

let getlists = () =>{

  var cities = ['Toronto','Edmonton','Vancouver','Chicago','Los_Angeles','New_York','Denver','Phoenix','Regina','Indianapolis','Winnipeg','Detroit', 'Montreal','Halifax'];
  var cit=(document.getElementById('city').value);
  //console.log((document.getElementById('city').value));
  val=(cities.includes(cit));
  if (val==false) {
    //console.log(val);
    document.getElementById('disp').style.display="block";
    document.getElementById('disp').innerHTML="Invalid Input";
  }
  if (val==true){
    document.getElementById('disp').disabled=true;
    document.getElementById('disp').innerHTML="Please Select Pokemon";
    dropwdownAjax(cit)
  }


}

$(function() {
  //console.log(document.querySelector('input'));
  //console.log('hi2');

  var elem = document.getElementById('city');
  elem.innerHTML="";
  elem.addEventListener('input', getlists);
});















const getlist = () =>{
  console.log('hi3')
  console.log(document.getElementById('city').value)
}

function SendAjax(){
    var form = document.querySelector("form");
    const data = formToJSON(form.elements);
    //console.log(data)
    //console.log(JSON.stringify(data, null, "  "));

    $.post('/hist',
        { data: data,
        processDataBoolean: false },
        function(data2, status, xhr) {
          console.log(data2/(data['bill']))
            if (data2/(data['bill'])<=0.14){
              temp=Math.round(data['bill']*0.14)
              document.getElementById("tip").innerHTML='Suggested total tip amount: '+temp;
            }else{
              document.getElementById("tip").innerHTML='Suggested total tip amount: '+data2;
            }
            form.reset()

            //alert('status: ' + status + ', data: ' + data);

        }).done(function() {  })
        .fail(function(jqxhr, settings, ex) { alert('failed, ' + ex); });
}


function dropwdownAjax(city){
    //var form = document.querySelector("form");
    //const data = formToJSON(form.elements);
    //console.log(data)
    //console.log(JSON.stringify(data, null, "  "));

    $.post('/dropdown',
        { data: city,
        processDataBoolean: false },
        function(data2, status, xhr) {
          data2=JSON.parse(data2);
          var options=""
          for (i = 0; i < data2.length; i++){
            options=options+'<option value="'+data2[i]+'">'+"\n"
          }
          //console.log(options)
          document.getElementById('poke_list').innerHTML=options;
          document.getElementById('poke').disabled=false;
        }).done(function() {  })
        .fail(function(jqxhr, settings, ex) { alert('failed to fetch pokemon, ' + ex); });
}
