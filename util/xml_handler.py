'''
对于xml文件的相关操作
'''
import xml.dom.minidom as Dom
from xml.dom import minidom
import xml.etree.ElementTree as ET
import os
import util.node


def fixed_writexml(self, writer, indent="", addindent="", newl=""):
    '''
    这个方法用来代替minidom里格式化代码，实现节点不换行
    :param self:
    :param writer:
    :param indent:
    :param addindent:
    :param newl:
    :return:
    '''
    writer.write(indent + "<" + self.tagName)
    attrs = self._get_attributes()
    a_names = attrs.keys()

    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        minidom._write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 \
                and self.childNodes[0].nodeType == minidom.Node.TEXT_NODE:
            writer.write(">")
            self.childNodes[0].writexml(writer, "", "", "")
            writer.write("</%s>%s" % (self.tagName, newl))
            return
        writer.write(">%s" % (newl))
        for node in self.childNodes:
            if node.nodeType is not minidom.Node.TEXT_NODE:
                node.writexml(writer, indent + addindent, addindent, newl)
        writer.write("%s</%s>%s" % (indent, self.tagName, newl))
    else:
        writer.write("/>%s" % (newl))


minidom.Element.writexml = fixed_writexml


def write_xml(object_list, dest_path):
    '''
    写到xml文件
    :param object_list: 装有Node对象的list
    :param dest_path: 目标文件
    :return: 无
    '''
    doc = Dom.Document()
    root_node = doc.createElement("annotation")
    doc.appendChild(root_node)

    for one in object_list:
        object_node = doc.createElement("object")

        name_node = doc.createElement("name")
        name_value = doc.createTextNode(one.name)
        name_node.appendChild(name_value)

        difficult_node = doc.createElement("difficult")
        difficult_value = doc.createTextNode(one.difficult)
        difficult_node.appendChild(difficult_value)

        bndbox = doc.createElement("bndbox")
        # bndbox中写入min_value
        xmin_node = doc.createElement("xmin")
        xmin_value = doc.createTextNode(one.xmin)
        xmin_node.appendChild(xmin_value)
        bndbox.appendChild(xmin_node)
        # bndbox中写入ymin_value
        ymin_node = doc.createElement("ymin")
        ymin_value = doc.createTextNode(one.ymin)
        ymin_node.appendChild(ymin_value)
        bndbox.appendChild(ymin_node)
        # bndbox中写入xmax_value
        xmax_node = doc.createElement("xmax")
        xmax_value = doc.createTextNode(one.xmax)
        xmax_node.appendChild(xmax_value)
        bndbox.appendChild(xmax_node)
        # bndbox中写入ymax_value
        ymax_node = doc.createElement("ymax")
        ymax_value = doc.createTextNode(one.ymax)
        ymax_node.appendChild(ymax_value)
        bndbox.appendChild(ymax_node)
        # obeject中写入name
        object_node.appendChild(name_node)
        # oject中写入difficult
        object_node.appendChild(difficult_node)
        # oject中写入bndbox
        object_node.appendChild(bndbox)
        # annotation中写入object_node
        root_node.appendChild(object_node)

    f = open(dest_path, "wb")
    f.write(doc.toprettyxml(indent="\t", newl="\n", encoding="utf-8"))
    f.close()



def read_xml(read_path, flag=False):
    '''
    读取一个文件夹下的所有xml文件
    :param read_path:
    :param flag: 决定是否需要读取number类型的node，默认为False
    :return: 装有对象类型为 node 的list
    '''
    node_list = []
    for file in os.listdir(read_path):
        file_path = os.path.join(read_path, file)
        in_file = open(file_path)
        tree = ET.parse(in_file)
        root = tree.getroot()

        for obj in root.iter('object'):
            cls = obj.find('name').text
            xmlbox = obj.find('bndbox')
            b = ((xmlbox.find('xmin').text), (xmlbox.find('ymin').text), (xmlbox.find('xmax').text),
                 (xmlbox.find('ymax').text))

            if cls == 'number' and flag == True:
                continue
            one = util.node.Node(cls, '0', b[0], b[1], b[2], b[3])
            node_list.append(one)
    return node_list


def integrate_xml(src_path_1, src_path_2, dest_path):
    '''
    将两份xml文件整合到一份里
    :param src_path_1:
    :param src_path_2:
    :param dest_path:
    :return:
    '''
    for file in os.listdir(src_path_1):
        dest_path = os.path.join(dest_path, file)
        node_list = read_xml(src_path_1)
        node_list += read_xml(src_path_2, True)
        write_xml(node_list, dest_path)


if __name__ == "__main__":
    read_xml()
