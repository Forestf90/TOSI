import javax.crypto.*;
import javax.crypto.spec.SecretKeySpec;
import java.math.BigInteger;
import java.security.*;
import java.util.Scanner;

public class Main {


    public static void main(String[] args) {

        System.out.println("Wpisz wiadomosc: ");
        Scanner in = new Scanner(System.in);
        String input = in.nextLine();
        //////////////////////////////
        System.out.println("Szyfrowanie za pomocą algorytmu DES: ");
        symmetricEncryption(input, "DES");
        System.out.println("Szyfrowanie za pomocą algorytmu RC4: ");
        symmetricEncryption(input, "RC4");

        //////////////////////////
        System.out.println("Szyfrowanie za pomocą algorytmu RSA: ");
        rsaEncryption(input);

        //////////////////////

        sha(input, "SHA-512");
        sha(input, "SHA3-512");

        //////////////////////////////////

        signature(input);
    }


    private static void symmetricEncryption(String massage, String algorithm) {

        try {
            KeyGenerator kGen = KeyGenerator.getInstance(algorithm);
            SecretKey sKey = kGen.generateKey();
            byte[] keyBytes = sKey.getEncoded();

            Cipher cipher = Cipher.getInstance(algorithm);

            cipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(keyBytes, algorithm));
            byte[] encrypted = cipher.doFinal(massage.getBytes());

            cipher.init(Cipher.DECRYPT_MODE, new SecretKeySpec(keyBytes, algorithm));
            byte[] decrypted = cipher.doFinal(encrypted);

            System.out.println("Wiadomosc zaszyfrowana: "+new String(encrypted));
            System.out.println("Wiadomosc odszyfrowana: "+new String(decrypted));


        } catch (NoSuchAlgorithmException | InvalidKeyException |
                IllegalBlockSizeException | BadPaddingException | NoSuchPaddingException e) {
            e.printStackTrace();
        }

    }


    private static void rsaEncryption(String massage) {

        try {
            KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("RSA");
            keyPairGenerator.initialize(2048);
            KeyPair keyPair = keyPairGenerator.generateKeyPair();
            PrivateKey privateKey = keyPair.getPrivate();
            PublicKey publicKey = keyPair.getPublic();

            Cipher cipher = Cipher.getInstance("RSA");
            cipher.init(Cipher.ENCRYPT_MODE, privateKey);
            byte[] encrypted = cipher.doFinal(massage.getBytes());

            cipher.init(Cipher.DECRYPT_MODE, publicKey);
            byte[] decrypted = cipher.doFinal(encrypted);

            System.out.println("Wiadomosc zaszyfrowana: "+new String(encrypted));
            System.out.println("Wiadomosc odszyfrowana: "+new String(decrypted));


        } catch (NoSuchAlgorithmException | InvalidKeyException |
                IllegalBlockSizeException | BadPaddingException | NoSuchPaddingException e) {
            e.printStackTrace();
        }

    }

    private static void sha(String massage, String type){
        try {
            MessageDigest md = MessageDigest.getInstance(type);
            byte[] messageDigest = md.digest(massage.getBytes());
            BigInteger no = new BigInteger(1, messageDigest);
            String hashtext = no.toString(16);
            while (hashtext.length() < 32) {
                hashtext = "0" + hashtext;
            }
            System.out.println("Wiadomosc zahashowana "+type+" : "+hashtext);

        }catch (Exception e){
            e.printStackTrace();
        }
    }

    private static void signature(String massage){

        try {

            KeyPairGenerator keyPairGen = KeyPairGenerator.getInstance("DSA");
            keyPairGen.initialize(2048);
            KeyPair pair = keyPairGen.generateKeyPair();
            PrivateKey privKey = pair.getPrivate();
            PublicKey pubKey = pair.getPublic();

            byte[] bytes = massage.getBytes();

            //Podpis
            Signature sign = Signature.getInstance("SHA256withDSA");
            sign.initSign(privKey);
            sign.update(bytes);
            byte[] signature = sign.sign();

            //weryfikacja
            Signature verify = Signature.getInstance("SHA256withDSA");
            verify.initVerify(pubKey);
            verify.update(bytes);
            verify.verify(signature);


        }catch (Exception e){
            e.printStackTrace();
        }
    }

}
