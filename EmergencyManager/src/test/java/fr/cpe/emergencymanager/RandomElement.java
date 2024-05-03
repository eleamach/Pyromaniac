package fr.cpe.emergencymanager;

import net.bytebuddy.utility.RandomString;

import java.util.List;

public class RandomElement {
    public static <T> T getRandomElement(List<T> list) {
        if (list == null || list.isEmpty()) {
            throw new IllegalArgumentException("La liste ne peut pas être nulle ou vide.");
        }

        java.util.Random random = new java.util.Random();
        int randomIndex = random.nextInt(list.size());

        return list.get(randomIndex);
    }

    public static String getRandomString(int length) {
        return RandomString.make(length);
    }

    public static void main(String[] args) {
        // Exemple d'utilisation avec une liste de chaînes
        List<String> stringList = List.of("Element1", "Element2", "Element3", "Element4", "Element5");

        String randomString = getRandomElement(stringList);
        System.out.println("Élément aléatoire : " + randomString);

        // Exemple d'utilisation avec une liste d'entiers
        List<Integer> integerList = List.of(1, 2, 3, 4, 5);

        Integer randomInteger = getRandomElement(integerList);
        System.out.println("Élément aléatoire : " + randomInteger);
    }
}