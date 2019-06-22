var $table;
var evt;
var changeIndex;
var titleList = new Array('Id','CourseId','CourseName','College');
var rows = new Array()

//初始化bootstrap-table的内容
function InitMainTable () {
    //记录页面bootstrap-table全局变量$table，方便应用
    var queryUrl = '/course/data?rnd=' + Math.random()
    $table = $('#table').bootstrapTable({
        editable:true,
        url: queryUrl,                      //请求后台的URL（*）
        method: 'GET',                      //请求方式（*）
        //toolbar: '#toolbar',              //工具按钮用哪个容器
        striped: true,                      //是否显示行间隔色
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        pagination: true,                   //是否显示分页（*）
        sortable: true,                     //是否启用排序
        sortOrder: "asc",                   //排序方式
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
        pageNumber: 1,                      //初始化加载第一页，默认第一页,并记录
        pageSize: 10,                     //每页的记录行数（*）
        pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
        paginationPreText: "Previous",
        paginationNextText: "Next",
        paginationFirstText: "First",
        paginationLastText: "Last",
        search: true,                      //是否显示表格搜索
        strictSearch: true,
        showColumns: true,                  //是否显示所有的列（选择显示的列）
        showRefresh: true,                  //是否显示刷新按钮
        minimumCountColumns: 2,             //最少允许的列数
        clickToSelect: true,                //是否启用点击选中行
        //height: 500,                      //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
        uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
        showToggle: true,                   //是否显示详细视图和列表视图的切换按钮
        cardView: false,                    //是否显示详细视图
        detailView: false,                  //是否显示父子表
        //得到查询的参数
        queryParams : function (params) {
            //这里的键的名字和控制器的变量名必须一致，这边改动，控制器也需要改成一样的
            var temp = {   
                rows: params.limit,                         //页面大小
                page: (params.offset / params.limit) + 1,   //页码
                sort: params.sort,      //排序列名 
                sortOrder: params.order //排位命令（desc，asc） 
            };
            return temp;
        },
        columns: [{
            checkbox: true,  
            visible: true                  //是否显示复选框  
        }, {
            field: 'Id',
            title: 'Id',
            sortable: true
        },{
            field: 'CourseId',
            title: '课程号',
            sortable: true
        }, {
            field: 'CourseName',
            title: '课程名',
            sortable: true
        }, {
            field:"College",
            title:"开课学院",
            sortable:true
        }, {
            field:'ID',
            title: '操作',
            width: 120,
            align: 'center',
            valign: 'middle',
            formatter: actionFormatter
        }],
        onLoadSuccess: function () {
            initTableEdit()
        },
        // onDblClickRow: function (row, $element) {
        //     console.log(row);
        // },
    });

    $('#addData').click(function(){
        $table.bootstrapTable('prepend',{0: undefined,new:true, CourseName: "", CourseId: "", College: ""});
        initTableEdit();
    });
};

//初始化表格编辑
function initTableEdit(){
    $('#table').editableTableWidget();
    $('table td').on('change',function(evt,newValue){
        if(newValue==undefined){
            window.changeIndex = evt.currentTarget.getElementsByTagName("input")[0].getAttribute('data-index');
        }else{
            if (evt.currentTarget.cellIndex<2 || evt.currentTarget.cellIndex>4){
                toastr.warning('禁止修改');
                return false;
            }
            title = window.titleList[evt.currentTarget.cellIndex - 1];
            row = window.rows[window.changeIndex];
            row[title] = newValue;
            if(row['new']!=true){
                $('span[data-index='+window.changeIndex+']')[0].innerHTML = "<a href='javascript:;' class='btn btn-xs blue' onclick=\"EditViewById("+window.changeIndex+")\" title='提交编辑'><span class='glyphicon glyphicon-pencil'></span></a>";
            }
           
        }
    });
}

//操作栏的格式化

function actionFormatter(value, row, index) {
    // console.log(row)
    // console.log(index)
    var result = "";
    window.rows[index] = row
    if(row['new']==true){
        result += "<a href='javascript:;' class='btn btn-xs red' onclick=\"AddById("+index+")\" title='添加'><span class='glyphicon glyphicon-ok'></span></a>";
    }else{
        result += "<span data-index='"+index+"'></span>"
        result += "<a href='javascript:;' class='btn btn-xs red' onclick=\"DeleteByIds("+index+")\" title='删除'><span class='glyphicon glyphicon-remove'></span></a>";
    }

    return result;
}

function DeleteByIds(index){
    console.log(window.rows[index])
    $.post(
        "delCourse",
        window.rows[index],
        function(data,status){
            data = JSON.parse(data);
            if(data['code']==1){
                toastr.info(data['result'])
            }else{
                toastr.error(data['result'])
            }
        }
    );
    document.getElementsByName("refresh")[0].click();
}

function EditViewById(index){
    console.log(window.rows[index]);
    $.post(
        "editCourse",
        window.rows[index],
        function(data,status){
            console.log(data)
            data = JSON.parse(data);
            if(data['code']==1){
                toastr.info(data['result'])
            }else{
                toastr.error(data['result'])
            }
        }
    );
    document.getElementsByName("refresh")[0].click();
}

function AddById(index){

    console.log(window.rows[index]);
    $.post(
        "addCourse",
        window.rows[index],
        function(data,status){
            console.log(data)
            data = JSON.parse(data);
            if(data['code']==1){
                toastr.info(data['result'])
            }else{
                toastr.error(data['result'])
            }
        }
    );
    document.getElementsByName("refresh")[0].click(); 
}

window.onload=function(){
    InitMainTable();
}
