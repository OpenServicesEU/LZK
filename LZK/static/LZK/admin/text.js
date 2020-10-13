django.jQuery(function() {
  var editor = CKEDITOR.replace(
    'id_body',
    {
      toolbarGroups: [
        { name: 'document', groups: [ 'mode', 'document', 'doctools' ] },
        { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
        { name: 'editing', groups: [ 'find', 'selection', 'spellchecker', 'editing' ] },
        { name: 'forms', groups: [ 'forms' ] },
        { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
        { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
        '/',
        { name: 'links', groups: [ 'links' ] },
        { name: 'insert', groups: [ 'insert' ] },
        { name: 'styles', groups: [ 'styles' ] },
        { name: 'colors', groups: [ 'colors' ] },
        { name: 'tools', groups: [ 'tools' ] },
        { name: 'others', groups: [ 'others' ] },
        { name: 'about', groups: [ 'about' ] }
      ],
      removeButtons: 'Save,Templates,NewPage,ExportPdf,Preview,Print,Scayt,Form,Checkbox,Radio,TextField,Textarea,Select,Button,ImageButton,HiddenField,Image,Flash,Smiley,SpecialChar,PageBreak,Iframe,About,CopyFormatting,RemoveFormat,SelectAll,Blockquote,CreateDiv,BidiLtr,BidiRtl,Language',
      width: 787,
    }
  );
  editor.on( 'contentDom', function() {
      editor.container.$.style.display = 'flex';
  });
});
