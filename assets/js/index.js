var $ = require("jquery");
import 'bootstrap';
import '../scss/cobweb.scss';
import fontawesome from '@fortawesome/fontawesome'
import solid from '@fortawesome/fontawesome-free-solid'

fontawesome.library.add(solid)

// Make TextAreas auto-sizing

$('textarea').each(function () {
  this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
}).on('input', function () {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
});
