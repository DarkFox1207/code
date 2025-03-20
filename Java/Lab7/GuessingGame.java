import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class GuessingGame extends JFrame {
    private int min;
    private int max;
    private int guess;
    private boolean cheating;
    private JLabel guessLabel;
    private JButton higherButton;
    private JButton lowerButton;
    private JButton correctButton;
    private JTextField minField;
    private JTextField maxField;
    private JButton startButton;

    private ButtonGroup lafGroup; // Группа для радиокнопок

    public GuessingGame() {
        setTitle("Игра в 'Больше-Меньше'");
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new FlowLayout());

        // Создание полей для ввода диапазона
        minField = new JTextField(5);
        maxField = new JTextField(5);
        startButton = new JButton("Начать игру");

        higherButton = new JButton("Больше");
        lowerButton = new JButton("Меньше");
        correctButton = new JButton("Угадал!");

        guessLabel = new JLabel("Введите диапазон чисел и нажмите 'Начать игру'");

        // Изначально скрываем кнопки ответа
        higherButton.setVisible(false);
        lowerButton.setVisible(false);
        correctButton.setVisible(false);

        // Добавление компонентов на панель
        add(new JLabel("Минимальное значение:"));
        add(minField);
        add(new JLabel("Максимальное значение:"));
        add(maxField);
        add(startButton);
        add(guessLabel);
        add(higherButton);
        add(lowerButton);
        add(correctButton);

        // Добавление радиокнопок для выбора Look and Feel
        JLabel lafLabel = new JLabel("Выберите оформление:");
        add(lafLabel);
        
        lafGroup = new ButtonGroup();
        String[] lafNames = { "Metal", "Nimbus", "CDE/Motif", "Windows", "Windows Classic" };
        for (String lafName : lafNames) {
            JRadioButton lafButton = new JRadioButton(lafName);
            lafButton.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    setLookAndFeel(lafName);
                }
            });
            lafGroup.add(lafButton);
            add(lafButton);
        }

        // Обработчик для кнопки "Начать игру"
        startButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                startGame();
            }
        });

        // Обработчики для кнопок ответа
        higherButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                min = guess + 1;
                makeGuess();
            }
        });

        lowerButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                max = guess - 1;
                makeGuess();
            }
        });

        correctButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (cheating) {
                    JOptionPane.showMessageDialog(null, "Вы жульничаете! Давайте сыграем еще раз.");
                } else {
                    JOptionPane.showMessageDialog(null, "Я угадал число! Давайте сыграем еще раз.");
                }
                resetGame();
            }
        });
    }

    private void setLookAndFeel(String lafName) {
        try {
            switch (lafName) {
                case "Metal":
                    UIManager.setLookAndFeel("javax.swing.plaf.metal.MetalLookAndFeel");
                    break;
                case "Nimbus":
                    UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                    break;
                case "CDE/Motif":
                    UIManager.setLookAndFeel("com.sun.java.swing.plaf.motif.MotifLookAndFeel");
                    break;
                case "Windows":
                    UIManager.setLookAndFeel("com.sun.java.swing.plaf.windows.WindowsLookAndFeel");
                    break;
                case "Windows Classic":
                    UIManager.setLookAndFeel("com.sun.java.swing.plaf.windows.WindowsClassicLookAndFeel");
                    break;
            }
            SwingUtilities.updateComponentTreeUI(this); // Обновляем интерфейс
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void startGame() {
        try {
            min = Integer.parseInt(minField.getText());
            max = Integer.parseInt(maxField.getText());

            if (min >= max) {
                JOptionPane.showMessageDialog(this, "Минимальное значение должно быть меньше максимального");
                return;
            }

            // Сброс состояния
            cheating = false;
            resetButtons();
            makeGuess();
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Введите валидные числа.");
        }
    }

    private void makeGuess() {
        guess = (min + max) / 2;
        guessLabel.setText("Я думаю, что это: " + guess);
        resetButtons();
        higherButton.setVisible(true);
        lowerButton.setVisible(true);
        correctButton.setVisible(true);
    }

    private void resetButtons() {
        higherButton.setVisible(false);
        lowerButton.setVisible(false);
        correctButton.setVisible(false);
    }

    private void resetGame() {
        minField.setText("");
        maxField.setText("");
        guessLabel.setText("Введите диапазон чисел и нажмите 'Начать игру'");
        resetButtons();
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            GuessingGame game = new GuessingGame();
            game.setVisible(true);
        });
    }
}