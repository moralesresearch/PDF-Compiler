import javax.swing.*;
import java.awt.*;
import java.awt.desktop.AboutHandler;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import org.apache.pdfbox.multipdf.PDFMergerUtility;

public class PDFCompiler extends JFrame {
    private JList<String> pdfList;
    private DefaultListModel<String> pdfListModel;
    private JLabel resultLabel;
    private HashMap<String, File> pdfPaths;

    public PDFCompiler() {
        pdfPaths = new HashMap<>();
        initUI();
        initMacOSAboutMenu();
    }

    private void initUI() {
        setTitle("PDF Compiler 3.0");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(400, 300);

        // Create layout
        Container contentPane = getContentPane();
        contentPane.setLayout(new BorderLayout());

        // Initialize the list and buttons
        pdfListModel = new DefaultListModel<>();
        pdfList = new JList<>(pdfListModel);
        JButton addButton = new JButton("Add PDFs");
        JButton combineButton = new JButton("Combine PDFs");
        resultLabel = new JLabel("");

        // Add components to layout
        JPanel buttonPanel = new JPanel();
        buttonPanel.add(addButton);
        buttonPanel.add(combineButton);

        contentPane.add(new JScrollPane(pdfList), BorderLayout.CENTER);
        contentPane.add(buttonPanel, BorderLayout.SOUTH);
        contentPane.add(resultLabel, BorderLayout.NORTH);

        // Button actions
        addButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                addPDFs();
            }
        });
        combineButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    combinePDFs();
                } catch (FileNotFoundException ex) {
                    throw new RuntimeException(ex);
                }
            }
        });
    }

    private void addPDFs() {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setMultiSelectionEnabled(true);
        fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
        int result = fileChooser.showOpenDialog(this);

        if (result == JFileChooser.APPROVE_OPTION) {
            File[] selectedFiles = fileChooser.getSelectedFiles();
            for (File file : selectedFiles) {
                if (file.getName().endsWith(".pdf")) {
                    pdfListModel.addElement(file.getName());
                    pdfPaths.put(file.getName(), file);
                }
            }
        }
    }

    private void combinePDFs() throws FileNotFoundException {
        List<File> selectedFiles = new ArrayList<>();
        for (int i = 0; i < pdfListModel.size(); i++) {
            String fileName = pdfListModel.getElementAt(i);
            selectedFiles.add(pdfPaths.get(fileName));
        }

        if (selectedFiles.isEmpty()) {
            resultLabel.setText("No PDF files to combine.");
            return;
        }

        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
        int result = fileChooser.showSaveDialog(this);

        if (result == JFileChooser.APPROVE_OPTION) {
            File outputFile = fileChooser.getSelectedFile();
            if (!outputFile.getName().endsWith(".pdf")) {
                outputFile = new File(outputFile.getPath() + ".pdf");
            }

            PDFMergerUtility pdfMerger = new PDFMergerUtility();
            for (File file : selectedFiles) {
                pdfMerger.addSource(file);
            }
            pdfMerger.setDestinationFileName(outputFile.getPath());

            try {
                pdfMerger.mergeDocuments(null);
                resultLabel.setText("Combined PDF saved as " + outputFile.getName());
            } catch (IOException e) {
                resultLabel.setText("Error combining PDFs.");
            }
        } else {
            resultLabel.setText("PDF combining cancelled.");
        }
    }

    private void initMacOSAboutMenu() {
        if (Desktop.isDesktopSupported()) {
            Desktop desktop = Desktop.getDesktop();
            if (desktop.isSupported(Desktop.Action.APP_ABOUT)) {
                desktop.setAboutHandler(new AboutHandler() {
                    @Override
                    public void handleAbout(java.awt.desktop.AboutEvent e) {
                        JOptionPane.showMessageDialog(
                                null,
                                "PDF Compiler\nVersion 3.0 (Spring 2024)\n" +
                                        "Released May 10, 2024\nCopyright (C) 2024 Morales Research " +
                                        "Technology Inc\nCopyright (C) 2023 - 24 The University of Texas at " +
                                        "Austin,\nDepartment of Computer Science",
                                "About PDF Compiler",
                                JOptionPane.INFORMATION_MESSAGE
                        );
                    }
                });
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            PDFCompiler pdfCompiler = new PDFCompiler();
            pdfCompiler.setVisible(true);
        });
    }
}
