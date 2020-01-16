console.log('hi')

const formToJSON = elements => [].reduce.call(elements, (data, element) => {
  data[element.name] = element.value;
  return data;
}, {});

if( document.readyState !== 'loading' ) {
    console.log( 'document is already ready, just execute code here' );
    init();
} else {
    document.addEventListener('DOMContentLoaded', function () {
        console.log( 'document was not ready, place code here' );
        init();
    });
}

function init() {
  console.log(document.querySelector('input'));
  console.log('hi2');
  var elem = document.getElementById('city');
  elem.addEventListener('input', getlist);
  console.log(document.querySelector('input'));
}

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
