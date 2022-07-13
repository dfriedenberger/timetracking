

//Time format functions

//returns YYYY-MM-DD format of date object
var dateToYMD = function (date) {
    var d = date.getDate();
    var m = date.getMonth() + 1; //Month from 0 to 11
    var y = date.getFullYear();
    return '' + y + '-' + (m <= 9 ? '0' + m : m) + '-' + (d <= 9 ? '0' + d : d);
}

//returns human readable Day "Mo, 17.11" format of date object 
var date_str = function (date) {

    var day = date.getDate();
    var month = date.getMonth() + 1;
    var wd = date.getDay();

    const days = ['So','Mo','Di','Mi','Do','Fr','Sa']
    var dayName = days[wd]
    return `${dayName}, ${day}.${month}`

}


//returns this week monday date object
var get_monday = function () {
    const today = new Date();
    const first = today.getDate() - today.getDay() + 1;
    return new Date(today.setDate(first));
}

//returns now as "HH:MM" format
var get_now = function () {
    const today = new Date();
    const h = today.getHours();
    const m = today.getMinutes();
    return (h <= 9 ? '0' + h : h) + ":" + (m <= 9 ? '0' + m : m)
}


//Create random Id e.g. for time spent entries
var random_id = function () {
    return "x" + Math.floor(Math.random() * 1000000000)
}

