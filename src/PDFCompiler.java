/*
Open Research License (ORL) Version 1.0

Copyright (c) 1999 - 2024 Morales Research Inc,
          (c) 2023 Erick Suarez,
          (c) 2023 - 2025 The University of Texas at Austin, Department of Computer Science

Preamble:

The Open Research License (ORL) is a permissive open source license designed to encourage collaboration, dissemination, and advancement of knowledge in the field of research and academia. This license aims to strike a balance between the principles of open sharing and the recognition of intellectual contributions. By using, modifying, or distributing software under the Open Research License, you agree to the terms and conditions outlined below.

License Terms and Conditions:

1. Definitions:

   1.1. "Licensed Software" refers to the software, code, or other creative works that are subject to this license.

   1.2. "Contributor" refers to any individual or entity that has contributed to the creation or modification of the Licensed Software.

2. Grant of Rights:

   2.1. Subject to the terms and conditions of this license, each Contributor hereby grants you a worldwide, royalty-free, non-exclusive license to use, reproduce, modify, distribute, and perform the Licensed Software, either in source code or object code form, for the purpose of research, study, teaching, and non-commercial activities.

   2.2. You may sublicense the rights granted under Section 2.1, provided that any such sublicense is consistent with the terms of this license.

3. Attribution and Recognition:

   3.1. In any publication, presentation, or distribution of research results that substantially uses or is based on the Licensed Software, you agree to provide proper attribution to the original Contributors. Such attribution shall include the names of the Contributors, the title of the Licensed Software, and a reference to this license.

4. Modification and Derivative Works:

   4.1. You may create and distribute modifications or derivative works of the Licensed Software, provided that:

      a) Your modifications are clearly indicated, and you do not claim them to be the original work of the original Contributors.
   
      b) You include prominent notices stating that you have modified the Licensed Software.
   
      c) You license your modifications or derivative works under the terms of this license or a compatible open source license.

5. No Warranty:

   5.1. The Licensed Software is provided "as is," without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. You use the Licensed Software at your own risk.

6. Limitation of Liability:

   6.1. In no event shall the Contributors be liable for any damages, whether in contract, tort, or otherwise, arising out of or in connection with the use or distribution of the Licensed Software.

7. Governing Law:

   7.1. This license shall be governed by and interpreted in accordance with the laws of the United States, excluding its conflict of law principles.

8. Modifications and Versions:

   8.1. The Contributors may release new versions or revisions of the Open Research License. You may choose to use any version of this license for the Licensed Software.

9. Termination:

   9.1. This license automatically terminates if you fail to comply with any of its terms and conditions. Upon termination, you must cease all use, distribution, and possession of the Licensed Software.

10. Entire Agreement:

   10.1. This license constitutes the entire agreement between the parties regarding its subject matter and supersedes all prior or contemporaneous understandings.
 */
import javax.swing.*;
import java.awt.*;
import java.awt.datatransfer.DataFlavor;
import java.awt.desktop.AboutHandler;
import java.awt.dnd.DnDConstants;
import java.awt.dnd.DropTarget;
import java.awt.dnd.DropTargetDragEvent;
import java.awt.dnd.DropTargetDropEvent;
import java.awt.dnd.DropTargetEvent;
import java.awt.dnd.DropTargetListener;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import org.apache.pdfbox.multipdf.PDFMergerUtility;

/**
 * This is the PDF Compiler classes that extends off JFrame to implement the user interface. This 
 * program is to compress/combine PDFs into one.
 * 
 * @author Abdon Morales (abdonm@cs.utexas.edu)
 * @version 3.1
 */
public class PDFCompiler extends JFrame {
    private JList<String> pdfList;
    private DefaultListModel<String> pdfListModel;
    private JLabel resultLabel;
    private HashMap<String, File> pdfPaths;

    /**
     * This is the PDFCompiler method/constructor that initializes the PDF paths into a hashmap 
     * ;and initializes the user interface (and the Apple's integrated about menu for the 
     * application.)
     */
    public PDFCompiler() {
        pdfPaths = new HashMap<>();
        initUI();
        initMacOSAboutMenu();
    }

    /**
     * This is the initUI private void method that creates the user interface using Java AWT's 
     * Swing library to build out the GUI such as the buttons, window, window size, and the 
     * "actions"/clicks.
     */
    private void initUI() {
        setTitle("PDF Compiler 3.1");
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

        /* Adding drag -n- drop file support */
        new DropTarget(pdfList, new DropTargetListener() {
            @Override
            public void dragEnter(DropTargetDragEvent dtde) {}

            @Override
            public void dragOver(DropTargetDragEvent dtde) {}

            @Override
            public void dropActionChanged(DropTargetDragEvent dtde) {}

            @Override
            public void dragExit(DropTargetEvent dte) {}

            @Override
            public void drop(DropTargetDropEvent dtde) {
                try {
                    dtde.acceptDrop(DnDConstants.ACTION_COPY);
                    List<File> droppedFiles = (List<File>) dtde.getTransferable().getTransferData(DataFlavor.javaFileListFlavor);
                    for (File file : droppedFiles) {
                        if (file.getName().endsWith(".pdf")) {
                            pdfListModel.addElement(file.getName());
                            pdfPaths.put(file.getName(), file);
                        }
                    }
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
            }
        });

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

    /**
     * This is the private void addPDFs() method that implements the functionality to the button 
     * "Add PDF" in the initUI method. This method also implements the File window to choose the 
     * PDF(s) and adding it to the list in the main window.
     */
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

    /**
     * This is the private void combinePDFs() method that implements the button "Combine PDFs" and 
     * creates the literal logic for combining the PDF using an open-source Java library called
     * Apache pdfbox. [This method throws an exception if the PDF is not found in specified path.]
     */
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

    /**
     * This the private void initMacOSAboutMenu() method that implements 
     * the information for the About window of the application.
     */
    private void initMacOSAboutMenu() {
        if (Desktop.isDesktopSupported()) {
            Desktop desktop = Desktop.getDesktop();
            if (desktop.isSupported(Desktop.Action.APP_ABOUT)) {
                desktop.setAboutHandler(new AboutHandler() {
                    @Override
                    public void handleAbout(java.awt.desktop.AboutEvent e) {
                        JOptionPane.showMessageDialog(
                                null,
                                """
                                        PDF Compiler
                                        Version 3.1
                                        Released May 16, 2024
                                        Copyright (C) 2024 Morales Research \
                                        Technology Inc
                                        Copyright (C) 2023 - 24 The University of Texas at \
                                        Austin,
                                        Department of Computer Science""",
                                "About PDF Compiler",
                                JOptionPane.INFORMATION_MESSAGE
                        );
                    }
                });
            }
        }
    }

    /**
     * This is the main entry point of the PDF Compiler Program.
     * @author Abdon Morales (abdonm@cs.utexas.edu)
     */
    public static void main(String[] args) {
        System.setProperty("apple.awt.application.name", "PDF Compiler");
        SwingUtilities.invokeLater(() -> {
            PDFCompiler pdfCompiler = new PDFCompiler();
            pdfCompiler.setVisible(true);
        });
    }
}
