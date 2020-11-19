Date.prototype.yymmdd = function() {
    var yy = this.getFullYear() - 2000;
    var mm = this.getMonth() + 1;
    var dd = this.getDate();
  
    return [yy, (mm>9 ? '' : '0') + mm, (dd>9 ? '' : '0') + dd].join('');
};

Date.prototype.hhmm = function() {
    var hh = this.getHours();
    var mm = this.getMinutes();
    var ss = this.getSeconds();
  
    return [(hh>9 ? '' : '0') + hh, (mm>9 ? '' : '0') + mm, (ss>9 ? '' : '0') + ss].join('');
};


