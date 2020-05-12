using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace Security
{
    class Program
    {

        static void Main(string[] args)
        {
            Console.WriteLine("Podaj wiadomosc do zaszyfrowania: ");
            String input = Console.ReadLine();

            SymmetricDES(input);
            SymmetricRC2(input);

            AsymetricRSA(input);

            Sha(input);

            Signature(input);

            Console.ReadLine();
        }


        static void SymmetricDES(String massage)
        {
            DES desEncrypt = DES.Create();
            desEncrypt.GenerateIV();
            desEncrypt.GenerateKey();
            ICryptoTransform cryptoTransformEn = desEncrypt.CreateEncryptor();
            byte[] mass = Encoding.ASCII.GetBytes(massage);
            byte[] encrypt = cryptoTransformEn.TransformFinalBlock(mass, 0, mass.Length);
            Console.WriteLine("Wiadomosc zaszyfrowana algorytmem DES:");
            Console.WriteLine(Encoding.ASCII.GetString(encrypt));


            DES desDecrypt = DES.Create();
            desDecrypt.Key = desEncrypt.Key;
            desDecrypt.IV = desEncrypt.IV;
            ICryptoTransform cryptoTransformDe = desDecrypt.CreateDecryptor();
            byte[] decrypt = cryptoTransformDe.TransformFinalBlock(encrypt, 0, encrypt.Length);
            Console.WriteLine("Wiadomosc odszyfrowana algorytmem DES:");
            Console.WriteLine(Encoding.ASCII.GetString(decrypt));


        }

        static void SymmetricRC2(String massage)
        {
            RC2 rc2Encrypt = RC2.Create();
            rc2Encrypt.GenerateIV();
            rc2Encrypt.GenerateKey();
            ICryptoTransform cryptoTransformEn = rc2Encrypt.CreateEncryptor();
            byte[] mass = Encoding.ASCII.GetBytes(massage);
            byte[] encrypt = cryptoTransformEn.TransformFinalBlock(mass, 0, mass.Length);
            Console.WriteLine("Wiadomosc zaszyfrowana algorytmem RC2:");
            Console.WriteLine(Encoding.ASCII.GetString(encrypt));


            RC2 rcDecrypt = RC2.Create();
            rcDecrypt.Key = rc2Encrypt.Key;
            rcDecrypt.IV = rc2Encrypt.IV;
            ICryptoTransform cryptoTransformDe = rcDecrypt.CreateDecryptor();
            byte[] decrypt = cryptoTransformDe.TransformFinalBlock(encrypt, 0, encrypt.Length);
            Console.WriteLine("Wiadomosc odszyfrowana algorytmem RC2:");
            Console.WriteLine(Encoding.ASCII.GetString(decrypt));

        }

        static void AsymetricRSA(String massage)
        {
            RSA rsa = RSA.Create();
            rsa.KeySize = 2048;
            byte[] mass = Encoding.ASCII.GetBytes(massage);

            byte[] encrypt = rsa.Encrypt(mass, RSAEncryptionPadding.OaepSHA1);
            Console.WriteLine("Wiadomosc zaszyfrowana algorytmem RSA:");
            Console.WriteLine(Encoding.ASCII.GetString(encrypt));

            byte[] decrypt = rsa.Decrypt(encrypt, RSAEncryptionPadding.OaepSHA1);
            Console.WriteLine("Wiadomosc odszyfrowana algorytmem RSA:");
            Console.WriteLine(Encoding.ASCII.GetString(decrypt));
        }


        static void Sha(String massage)
        {
            SHA256 sha256 = SHA256.Create();

            byte[] mass = Encoding.ASCII.GetBytes(massage);
            byte[] mass256 = sha256.ComputeHash(mass);

            SHA1 sha1 = SHA1.Create();
            byte[] mass1 = sha1.ComputeHash(mass);

            Console.WriteLine("Wiadomosc zahashowana SHA256:");
            Console.WriteLine(Encoding.ASCII.GetString(mass256));
            Console.WriteLine("Wiadomosc zahashowana SHA1:");
            Console.WriteLine(Encoding.ASCII.GetString(mass1));

        }

        static void Signature(String massage)
        {
            RSA rsa = RSA.Create();
            rsa.KeySize = 2048;
            byte[] mass = Encoding.ASCII.GetBytes(massage);

            byte[] encrypt = rsa.Encrypt(mass, RSAEncryptionPadding.OaepSHA1);
            byte[] decrypt = rsa.Decrypt(encrypt, RSAEncryptionPadding.OaepSHA1);


            SHA256 sha256 = SHA256.Create();
            byte[] hash = sha256.ComputeHash(encrypt);

            RSAPKCS1SignatureFormatter formatter = new RSAPKCS1SignatureFormatter(rsa);
            formatter.SetHashAlgorithm("SHA256");
            byte[] signature = formatter.CreateSignature(hash);

            //////////////////

            RSA rsaDecrypt = RSA.Create();
            rsaDecrypt.ImportParameters(rsa.ExportParameters(true));

            RSAPKCS1SignatureDeformatter formatter2 = new RSAPKCS1SignatureDeformatter(rsaDecrypt);
            formatter2.SetHashAlgorithm("SHA256");
            formatter2.VerifySignature(hash, signature);

        }

    }
}
