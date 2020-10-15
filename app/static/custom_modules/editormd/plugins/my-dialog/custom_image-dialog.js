// custom_image-dialog.js



(function() {

    var factory = function (exports) {

		var pluginName   = "custom_image-dialog";

		exports.fn.customImageDialog = function() {

			var _this       = this;
			var cm          = this.cm;
            var editor      = this.editor;
            var settings    = this.settings;
            var selection   = cm.getSelection();
            var lang        = this.lang;
            var imageLang    = lang.dialog.image;
            var classPrefix = this.classPrefix;
			var dialogName  = classPrefix + pluginName, dialog;

			cm.focus();

            if (editor.find("." + dialogName).length > 0)
            {
                dialog = editor.find("." + dialogName);
                dialog.find("[data-url]").val("http://");

                this.dialogShowMask(dialog);
                this.dialogLockScreen();
                dialog.show();
            }
            else
            {
                var dialogHTML = "<div class=\"" + classPrefix + "form\">" + 
                                        "<label>" + imageLang.url + "</label>" + 
                                        "<input type=\"text\" value=\"http://\" data-url />" +
                                        "<br/>" + 
                                        "<input id=\"file-selector\" type=\"file\" accept=\".jpg, .jpeg, .png\" />" +
                                        "<br/>" + 
                                    "</div>";

                dialog = this.createDialog({
                    title      : imageLang.title,
                    width      : 380,
                    height     : 211,
                    content    : dialogHTML,
                    mask       : settings.dialogShowMask,
                    drag       : settings.dialogDraggable,
                    lockScreen : settings.dialogLockScreen,
                    maskStyle  : {
                        opacity         : settings.dialogMaskOpacity,
                        backgroundColor : settings.dialogMaskBgColor
                    },
                    buttons    : {
                        enter  : [lang.buttons.enter, function() {

                            var fileSelector   = document.getElementById('file-selector');

                            if (fileSelector.files[0] == null) {
                                alert("입력하고 싶은 사진 파일을 먼저 선택해주세요.")
                                return false;
                            }
                            else {
                                // 저장되는 파일 이름 형식: userName_yymmdd_hhmm.jpg
                                var userName = 'test'

                                var d = new Date()
                                var timeStamp = d.yymmdd()+'_'+d.hhmm()

                                var inputName = fileSelector.files[0].name
                                var len = inputName.length
                                var dot = inputName.lastIndexOf('.')
                                var inputExtension = inputName.substring(dot, len).toLowerCase()

                                var fileName = userName+'_'+timeStamp+inputExtension

                                var upload = new AWS.S3.ManagedUpload({
                                    params: {
                                        Bucket: 'ppt-maker-bucket',
                                        Key: 'editorInputImage/' + fileName,
                                        Body: fileSelector.files[0],
                                        ACL: "public-read"
                                    }
                                });

                                var promise = upload.promise();

                                promise.then(
                                    function (data) {

                                        var url = "https://ppt-maker-bucket.s3.ap-northeast-2.amazonaws.com/editorInputImage/"+fileName
                                        var str = "![](" + url + ")";
                                        cm.replaceSelection(str);

                                        alert("input: " + fileSelector.files[0].name + " / file: "+fileName);
                                    },
                                    function (err) {
                                        return alert(err);
                                    }
                                );

                            }

                            // var url   = this.find("[data-url]").val();

                            // if (url === "http://" || url === "")
                            // {
                            //     alert(imageLang.urlEmpty);
                            //     return false;
                            // }
                            
                            // var str = "![](" + url + ")";
                            
                            // cm.replaceSelection(str);

                            this.hide().lockScreen(false).hideMask();

                            return false;
                        }],

                        cancel : [lang.buttons.cancel, function() {                                   
                            this.hide().lockScreen(false).hideMask();

                            return false;
                        }]
                    }
                });
			}
		};

	};
    
	// CommonJS/Node.js
	if (typeof require === "function" && typeof exports === "object" && typeof module === "object")
    { 
        module.exports = factory;
    }
	else if (typeof define === "function")  // AMD/CMD/Sea.js
    {
		if (define.amd) { // for Require.js

			define(["editormd"], function(editormd) {
                factory(editormd);
            });

		} else { // for Sea.js
			define(function(require) {
                var editormd = require("./../../editormd");
                factory(editormd);
            });
		}
	} 
	else
	{
        factory(window.editormd);
	}

})();
