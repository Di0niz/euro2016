// определяем компонент, который читает список команд и отображет их

"use strict";


var CommandItem = React.createClass({

    // определяем доступ к глобальному контексту
    contextTypes: {
        commands: React.PropTypes.object
    },    

    render: function() {

        var command = this.context.commands[this.props.data]

        var ret;

        if (this.props.align==="left") {
            ret =<span className="command_title">{command.name}<img className={"flag " + command.small_picture} src="/img/blank.gif"/></span> 
        } else {
            ret =<span className="command_title"><img className={"flag " + command.small_picture} src="/img/blank.gif"/>{command.name}</span> 
        }   
        return ret;

    }

});


// Correct :)
var CommandItemWrapper = React.createClass({
  render: function() {
    return <CommandItem data={this.props.data}></CommandItem>
  }
});

var CommandList = React.createClass({

    render: function() {

        var commandNodes = this.props.data.map( 
            (result, i) => ( <CommandItemWrapper key={i} data={result}/>));
        return <span>{commandNodes}</span>
    }

});


var MatchItem = React.createClass ({
    render: function () {

        var match = this.props.data;
        var d = new Date(match.matchTime);
        return <div><table class="border_match"><thead><tr><th class="border_match_left"><CommandItem data={match.firstCommand} align="left"/></th>
<th class="border_match_right"><CommandItem data={match.secondCommand} align="right"/></th>
        </tr>
        <tr><td colspan="2">{d.toLocaleString()}</td></tr>
     </thead></table></div>

    }

});


var MatchItemWrapper = React.createClass ({
    render: function () {
        return <MatchItem data={this.props.data}/> 
    }
});

var MatchList= React.createClass ({
    render: function () {
        var items = this.props.data.map(
            
            (result)=>( <MatchItemWrapper key={result.firstCommand+ "_" + result.secondCommand} data={result}/>)
            );

        return <div>{items}</div>;
    }
});



/*


    RoundsTable
        RoundHeader param
        RoundRow1
        RoundRow2-n
*/

var UserItem = React.createClass ({
    render: function () {
        return <li>{this.props.data.altTitle}</li> 
    }
});


var UserItemWrapper = React.createClass ({
    render: function () {
        return <UserItem data={this.props.data}/> 
    }
});

var UserList = React.createClass({

    render: function () {

        var obj = this.props.data;

        var items = Object.keys(obj).map(key => <UserItemWrapper key={key} data={obj[key]}/> )

       // var items = this.props.data.map ( (r,i) => ( <UserItemWrapper key={i} data={r}/> ));

        return <ul>{items}</ul>;
        
    }


}); 


var RoundsTable = React.createClass({

    childContextTypes: {
        commands: React.PropTypes.object,
        users: React.PropTypes.object
    },    
    getChildContext() {
        return {
            commands: this.state.data.commands,
            users:  this.state.data.users
        };
    },

    getInitialState: function() {
        return {data: {"commands":{}, "matches":[], "users":{}}};
    },
    componentDidMount: function() {

        // считываем данные из таблицы
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function(data) {
                // сортируем данных
                data.matches = data.matches.sort((a,b)=>( a.endTime > b.endTime) );

                this.setState({data: data});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
      }, 
    

  render: function() {
    return (
      <div>

       <MatchList data={this.state.data.matches} commands={this.state.data.commands} /> 

       <UserList data={this.state.data.users}/>
      </div>
    );
  }

});


var { Cell, Column, ColumnGroup, Table} = FixedDataTable;


class MyTable extends React.Component {
  render() {
    return (
      <Table
        rowsCount={5}
        rowHeight={50}
        width={1000}
        height={500}>
        <Column
          cell={<Cell>Basic content</Cell>}
          width={200}
        />
      </Table>
    );
  }
}
/*
ReactDOM.render(
  <RoundsTable url="/api/round/5084141766836224.json"/>,
  document.getElementById('content')
);
*/

ReactDOM.render(
  <MyTable />,
  document.getElementById('content')
);