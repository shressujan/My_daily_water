filePath = '../../tmp/states.txt';
//function readTextFile()
//{
//    //Initialize the FileReader object to read the 2file
//    var fileReader = new FileReader();
//    var blob = new Blob(["Hello world!"], { type: "text/plain" });
//    var sampleFile = new File(blob, 'sample.txt');
//    fileReader.onload = function(event) {
//    var contents = event.target.result;
//    console.log("File contents: " + contents);
//    };
//
//    fileReader.onerror = function(event) {
//        console.error("File could not be read! Code " + event.target.error.code);
//    };
//    console.log(fileReader.readAsText(sampleFile));
//}

function readFile() {
    $.ajax({
    url: filePath,
    type: 'GET',
    dataType: 'text',
    success: function(data){
        console.log(data);
    }
    });
}