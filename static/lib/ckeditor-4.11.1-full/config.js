/**
 * @license Copyright (c) 2003-2018, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
    config.language = "zh-cn";
    config.toolbar = [
		//{ name: 'document', items: [ 'Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates' ] },
		//{ name: 'clipboard', items: [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ] },
		//{ name: 'editing', items: [ 'Find', 'Replace', '-', 'SelectAll', '-', 'Scayt' ] },
		//{ name: 'forms', items: [ 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField' ] },

		{ name: 'basicstyles', items: [ 'Bold', 'Italic', 'Underline', 'Strike' ] }, //'Subscript', 'Superscript', '-', 'CopyFormatting', 'RemoveFormat' ] },
        { name: 'colors', items: [ 'TextColor', 'BGColor' ] },
        { name: 'paragraph', items: [ 'Outdent', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'NumberedList', 'BulletedList', ] },// 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'BidiLtr', 'BidiRtl', 'Language' ] },
		{ name: 'links', items: [ 'Link',] },// 'Unlink', 'Anchor' ] },//
		{ name: 'insert', items: [ 'Image', 'Table', 'HorizontalRule',  'SpecialChar' ] },

		{ name: 'styles', items: [ 'Format', 'Font', 'FontSize' ] },
		{ name: 'tools', items: [ 'Maximize',] },// 'ShowBlocks' ] },
	];
    config.filebrowserUploadUrl= "/workbench/upload/?from=ckeditor&type=img"

    config.tabSpaces = 4;// in edit, replace [tab] with 4 [space]
    config.bodyClass = 'document-editor';// ckeditor-body class
    config.contentsCss = ['/static/dist/CSS/ckeditor_style.css'];// required stylesheet
    config.extraPlugins = [
        'tableresize',
        'autogrow',
    ].join(",");
    config.autoGrow_minHeight = 200;
    config.autoGrow_maxHeight = 500;
};
