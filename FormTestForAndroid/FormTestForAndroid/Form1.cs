using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Windows.Forms;

namespace FormTestForAndroid
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        Socket clientSocket;
        int clickCgFlag = 0;
        private void loginButton_Click(/*object sender, EventArgs e*/)
        {
            string ipStr = this.textBox1.Text.Trim();
            IPAddress ip = IPAddress.Parse(ipStr);
            clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            clientSocket.SendTimeout = 1000;         //连接和发送时间超过500ms则失败了。
            clientSocket.ReceiveTimeout = 3000;     //如果发送之后3s钟没有人回复，则断开了。
            int connPort = Int16.Parse((14578).ToString());
            try
            {
                clientSocket.Connect(new IPEndPoint(ip, connPort)); //配置服务器IP与端口 

                if (clickCgFlag++ > 50)
                    clickCgFlag = 0;
                byte[] arrFileSend = new byte[10 + 1];
                for (int i = 0; i < 5; i++)
                {
                    arrFileSend[i] = (byte)(65 + i); // 用来表示发送的是文件数据；
                    arrFileSend[i+5] = (byte)(65 + clickCgFlag);
                }
                
                clientSocket.Send(arrFileSend);
            }
            catch (Exception)
            {
                tvShowMessage.Text = "网络不可打开(可能被连接了),或者发送不成功。";
                return;
                // throw;
            }

            // 定义一个2M的缓存区；
            byte[] arrMsgRec = new byte[200];
            int length = -1;
            try
            {
                // 将接受到的数据存入到输入  arrMsgRec中；               
                length = clientSocket.Receive(arrMsgRec); // 接收数据，并返回数据的长度；
                var str = System.Text.Encoding.Default.GetString(arrMsgRec);
                tvShowMessage.Text = str.ToString();
            }
            catch (SocketException se)
            {
                tvShowMessage.Text = "网络接收超时！";
                return;
                //throw;
                //ShowMsg("异常；" + se.Message); return;
            }
            if (clientSocket.Connected)
                clientSocket.Close();

            //writeLog("连接服务器成功");
            //button_createConn.Text = "断开连接";
            //开启监听线程
            /*
          */

            /*
            Socket serverSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            serverSocket.Bind(new IPEndPoint(IPAddress.Parse("127.0.0.1"), 12234));  //绑定IP地址：端口  
            serverSocket.Listen(10);//设定最多10个排队连接请求  
            */
        }
        private void button1_Click(object sender, EventArgs e)
        {
            loginButton_Click();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {
            if (clientSocket != null && clientSocket.Connected)
            {
                clientSocket.Close();
                clientSocket.Dispose();
            }
            if (checkBox1.Checked)
            {
                this.textBox1.Text = "127.0.0.1";
            }
            else
                this.textBox1.Text = "66.98.119.26";
        }
    }
}
