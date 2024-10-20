import xml.etree.ElementTree as ET
from typing import Any, Callable, List, Dict, Optional, Union

class XMLParser:
    def __init__(self, xml_data: str):

        try:
            self.tree = ET.ElementTree(ET.fromstring(xml_data))
            self.root = self.tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"Error parsing XML: {e}")
        
    def __get_element_attr(self, element: ET.Element, attribute: str, default: Any = None, data_type: Callable[[str], Any] = str) -> Any:

        if element is None or attribute not in element.attrib:
            return default
        try:
            return data_type(element.attrib[attribute])
        except (ValueError, TypeError):
            return default

    def __get_element_value(self, element: Optional[ET.Element], data_type: Callable[[str], Any], default: Any) -> Any:
        if element is None or element.text is None:
            return default
        try:
            return data_type(element.text)
        except (ValueError, TypeError):
            return default
        
    def __find(self, tag: str) -> Optional[ET.Element]:
        return self.root.find(tag) if tag not in ["./", ".", ""] else self.root

    def val(self, tag: str, default: Any = None, data_type: Callable[[str], Any] = str) -> Any:
        element = self.root.find(tag)
        return self.__get_element_value(element, data_type, default)

    def attr(self, tag: str, attribute: str, default=None, data_type=str):
        element = self.__find(tag)
        return self.__get_element_attr(element, attribute, default=default, data_type=data_type)

    def list_of_val(self, tag: str, data_type: Callable[[str], Any] = str) -> List[Any]:

        elements = self.root.findall(tag)
        return [self.__get_element_value(element, data_type, None) for element in elements if element is not None and element.text is not None]

    def list_of_attr(self, tag: str, attribute: str, data_type: Callable[[str], Any] = str) -> List[Any]:

        elements = self.root.findall(tag)
        return [self.__get_element_attr(element, attribute, data_type=data_type) for element in elements if element is not None and attribute in element.attrib]

    def list_of_dict(self, tag: str, attributes: Dict[str, Union[Callable[[str], Any], tuple]]) -> List[Dict[str, Any]]:

        elements = self.root.findall(tag)
        result = []

        for element in elements:
            item = {}
            for attr_name, attr_info in attributes.items():
                if isinstance(attr_info, tuple):
                    default, data_type = attr_info
                else:
                    default, data_type = None, attr_info
                
                item[attr_name] = self.__get_element_attr(element, attr_name, default=default, data_type=data_type)
            result.append(item)

        return result


    def list_of_name(self, parent_tag: str) -> List[str]:
        parent_element = self.root.find(parent_tag)
        if parent_element is None:
            return []
        
        return [child.tag for child in parent_element]

    def extract_as_list(self, tag: str) -> List[str]:
        elements = self.root.findall(tag)
        return [ET.tostring(element, encoding='unicode', method='xml') for element in elements]