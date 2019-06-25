var $table;
var evt;
var changeIndex;
var titleList = new Array('Source');
var rows = new Array()

//初始化bootstrap-table的内容
function InitMainTable () {
    //记录页面bootstrap-table全局变量$table，方便应用
    var queryUrl = '/source/data?rnd=' + Math.random()
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
        clickToSelect: false,                //是否启用点击选中行
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
        }, {
            field: 'StudentId',
            title: '学号',
            sortable: true
        }, {
            field: 'StudentName',
            title: '姓名',
            sortable: true
        }, {
            field:'_class',
            title:'班级',
            sortable:true
        }, {
            field:"CourseId",
            title:"课程号",
            sortable:true
        }, {
            field:'CourseName',
            title:'课程',
            sortable:true
        }, {
            field:"Source",
            title:"成绩",
            class:'Source',
            sortable:true
        },{
            field:'ID',
            class:'ID',
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


};

//初始化表格编辑
function initTableEdit(){
    $('#table').editableTableWidget();



    $('table td').on('change',function(evt,newValue){

        window.evt = evt;
        window.changeIndex = evt.currentTarget.parentElement.getAttribute('data-index');
        if(window.changeIndex!=undefined){
            classList = evt.currentTarget.classList
            row = rows[window.changeIndex];

            for(var i=0;i<classList.length;i++){
                if($.inArray(classList[i],window.titleList)>-1){

                    row[classList[i]] = evt.currentTarget.innerText;
                    if(classList[i]=='Sex'){
                        if(evt.currentTarget.innerText=='女'){
                            row[classList[i]]=true
                        }else{
                            row[classList[i]]=false
                        }
                    }
                    $('span[data-index='+window.changeIndex+']')[0].innerHTML = "<a href='javascript:;' class='btn btn-xs blue' onclick=\"EditViewById("+window.changeIndex+")\" title='提交编辑'><span class='glyphicon glyphicon-pencil'></span></a>";
                    return true;
                }
            }
        }else{
            return false;
        }
        toastr.warning('禁止修改');
        return false;
    });

}

//操作栏的格式化

function actionFormatter(value, row, index) {
    // console.log(row)
    // console.log(index)
    var result = "";
    window.rows[index] = row
    result += "<span data-index='"+index+"'></span>"

    return result;
}





function EditViewById(index){
    console.log(window.rows[index]);
    $.post(
        "editSource",
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

