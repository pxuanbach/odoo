/** @odoo-module */
import { Component} from "@odoo/owl";
import { renderToElement } from "@web/core/utils/render";
import { registry } from "@web/core/registry";

export class CategColorField extends Component {
  setup() {
    this.totalColors = [1,2,3,4,5,6];
    super.setup();
 }
 clickPill(value) {
   this.props.record.update({ [this.props.name]: value });
 }
 categInfo(ev){
  var $target = $(ev.target);
  var data = $target.data();
  $target.parent().find(".categInformationPanel").html($(renderToElement("CategInformation",{
      value: data.value,
      'widget': this
  })));
}
}

CategColorField.template = "CategColorField";
CategColorField.supportedTypes = ["integer"];

registry.category("fields").add("category_color", {
  component: CategColorField,
});
