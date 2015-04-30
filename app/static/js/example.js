var example = (function(){
    var links = [];

    $.template( "nodeTemplate", '<li><span class="glyphicon glyphicon-asterisk" aria-hidden="true"></span> id: ${id}, name: ${name}</li>');
    $.template( "edgeTemplate", '<li><span class="glyphicon glyphicon-resize-horizontal" aria-hidden="true"></span> soruce: ${source}, target: ${target}</a></li>');

    function testList() {

        $.ajax({
            'type': 'GET',
            'data': {},
            'url': '/example/data'
        }).success(function(data){

            console.log(JSON.stringify(data));

            var $a = $("#example_list");
            $a.empty();
            $.tmpl( "nodeTemplate", data.nodes).appendTo($a);
            $.tmpl( "edgeTemplate", data.edges).appendTo($a);
        });


    }

    return {
        'test_list': function(){testList()},

        'register_events': function() {
            $('#example_button').click(function(evt){
                evt.preventDefault();
                testList();
            });
        }
    }
})();