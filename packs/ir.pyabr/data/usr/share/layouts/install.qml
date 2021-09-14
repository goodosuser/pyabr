import QtQuick 2.0
import QtQuick.Window 2.3
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.4
import QtQuick.Controls 1.2
import QtQuick.Controls 2.3
import QtQuick.Controls.Styles 1.4

ApplicationWindow {
    id: ask
    visible: true
    color: "white"

    width: 500
    height: 200

    Rectangle {
        id: txtText
        width: parent.width
        height: parent.height/2
        
        Image {
            source: 'file:///stor/usr/share/icons/breeze-archive.svg'
            anchors.left: parent.left
            anchors.leftMargin: 20
            id: imagex
            objectName: "logo"
            anchors.rightMargin: 20
            height: parent.height
            width: parent.height
            sourceSize: Qt.size( imagex.width, imagex.height )
        }

        Text {
            anchors.left: imagex.right
            text: "Commento"
            font.family: "IRANSans"
            font.pixelSize: 30
            anchors.leftMargin: 20
            objectName: "name"
            anchors.rightMargin: 20
            anchors.topMargin: 20
            anchors.top: parent.top
            id: titlex
        }

        Text {
            color: "gray"
            anchors.left: imagex.right
            font.family: "IRANSans"
            anchors.leftMargin: 20
            anchors.rightMargin: 20
            objectName: "descriptionx"
            anchors.top: titlex.bottom
        }

        ProgressBar {
            anchors.top: parent.top
            width: parent.width
            height: 10
            indeterminate: true
            objectName: "pro"
            visible: false
        }

        anchors.topMargin: 5
        anchors.rightMargin: 5
        anchors.leftMargin: 5
        anchors.top: parent.top
    }
    Button {
        id: cancel
        text: "No"
        objectName: "btnCancel"
        font.family: "IRANSans"
        width: parent.width/2
        height: parent.height/4
        anchors.bottom: parent.bottom
    }
    Button {
        text: "Yes"
        objectName: "btnOK"
        width: parent.width/2
        font.family: "IRANSans"
        height: parent.height/4
        anchors.left: cancel.right
        anchors.bottom: parent.bottom
    }
}