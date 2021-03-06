# coding=utf-8
import datetime
import zipfile

import gi, conexion, variables, funcionesCli, funcionesHab, zipfile, shutil, os, funcionesReservas, impresion, datetime, funcionesServicios, xlrd, xlwt
from gi.repository import Gtk, Gdk
from subprocess import call
from datetime import datetime
gi.require_version('Gtk','3.0')

class Eventos:


 # Eventos Generales

    def salir(self):
        conexion.Conexion().cerrarBBDD()
        Gtk.main_quit()

    # ---------------------------------------------------------------

    def on_vPrincipal_destroy(self,widget):
        self.salir()

    # ---------------------------------------------------------------

    def on_btnSalirTool_clicked(self,widget):
        conexion.Conexion().cerrarBBDD()
        Gtk.main_quit()

    # ---------------------------------------------------------------

    def on_btnAltas_clicked(self,widget):
        try:
            dni = variables.filacli[0].get_text()
            apel = variables.filacli[1].get_text()
            nombre = variables.filacli[2].get_text()
            fecha = variables.filacli[3].get_text()
            registro = (dni,apel,nombre,fecha)

            if dni != '' and apel != '' and nombre !='':
                if funcionesCli.validarDNI(dni):
                    funcionesCli.insertarcli(registro)
                    funcionesCli.listadocli(variables.listclientes)
                    funcionesCli.clearEntry(variables.filacli)

        except Exception as e:
            print("Error alta cliente", e)

    # ---------------------------------------------------------------

    def on_btnBajas_clicked(self,widget):
        try:
            dni = variables.filacli[0].get_text()

            if dni != '':
                funcionesCli.bajaCli(dni)
            else:
                print("dni inexistente")
        except:
            print('Error baja cliente')

    # ---------------------------------------------------------------

    def on_btnModificar_clicked(self,widget):
        try:
            cod = variables.lblerrordni[1].get_text()
            dni = variables.filacli[0].get_text()
            apellido =  variables.filacli[1].get_text()
            nombre =  variables.filacli[2].get_text()
            fecha = variables.filacli[3].get_text()
            registro = (dni,apellido,nombre,fecha)

            if dni != '':
                funcionesCli.modifCli(registro,cod)
                funcionesCli.listadocli(variables.listclientes)
                funcionesCli.clearEntry(variables.filacli)
            else:
                print("Dni Inexistente")

        except Exception as e:
            print("Error en modificar",e)

    # ---------------------------------------------------------------


    def on_treeClientes_cursor_changed(self, widget):

        try:
            model, iter = variables.treeclientes.get_selection().get_selected()
            # model es el modelo de la tabla de datos
            # iter es el número que identifica a la fila que marcamos

            if iter != None:
                sdni = model.get_value(iter, 0)
                sapel = model.get_value(iter, 1)
                snombre = model.get_value(iter, 2)
                sfecha = model.get_value(iter, 3)
                cod = funcionesCli.selectcli(sdni)
                variables.lblerrordni[1].modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('blue'))
                variables.lblerrordni[1].set_text(str(cod[0]))
                variables.filacli[0].set_text(sdni)
                variables.filacli[1].set_text(sapel)
                variables.filacli[2].set_text(snombre)
                variables.filareserva[0].set_text(sdni)
                variables.filareserva[1].set_text(sapel+" "+snombre)
                if sfecha != None:
                    variables.filacli[3].set_text(str(sfecha))
                else:
                    variables.filacli[3].set_text("")

        except Exception as e:
            print(e)

    # ---------------------------------------------------------------

    def on_entDni_focus_out_event(self, widget, Data=None):

        self.var = variables.filacli[0].get_text()

        if funcionesCli.validarDNI(self.var):
            variables.lblerrordni[0].modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('green'))
            variables.lblerrordni[0].set_text("DNI CORRECTO")

        else:
            variables.lblerrordni[0].modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('red'))
            variables.lblerrordni[0].set_text("DNI INCORRECTO")

    # ---------------------------------------------------------------


    def on_btnCalendar_clicked(self,widget):
        try:
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
            variables.semaforo = 1
        except Exception as e:
            print("Error abrir calendario",e)

    # ---------------------------------------------------------------

    def on_Calendar_day_selected_double_click(self,widget):
        try:
            panelactual = variables.panel.get_current_page()
            year, mes, dia = variables.calendar.get_date()
            fecha = "%s/" % dia + "%s/" % (mes + 1) + "%s" % year

            if variables.semaforo == 1:
                variables.filacli[3].set_text(fecha)
            elif variables.semaforo == 2:
                variables.filareserva[2].set_text(fecha)
                funcionesReservas.calculardias()
            elif variables.semaforo == 3:
                variables.filareserva[3].set_text(fecha)
                funcionesReservas.calculardias()


        except Exception as e:
            print("error fecha seleccionada",e)

    # ---------------------------------------------------------------

    # Eventos Habitaciones


    def on_btnAltasHabitacion_clicked(self, widget):
        try:
            numero = variables.filahab[0].get_text()
            precio = variables.filahab[1].get_text()
            tipo = None

            if variables.filarbt[0].get_active() == True:
                tipo = 'Simple'
            elif variables.filarbt[1].get_active() == True:
                tipo = 'Double'
            elif variables.filarbt[2].get_active() == True:
                tipo = 'Familiar'

            registro = (numero, tipo, precio)

            if numero != '' and precio != '':
                funcionesHab.insertarhab(registro)
                funcionesHab.listadohab(variables.listhabitaciones)
                funcionesHab.clearEntry(variables.filahab)
                variables.cmbreserhabitacion.set_active(0)
                funcionesReservas.listadonumhab(self)

        except Exception as e:
            print("Error alta habitacion", e)

    # ---------------------------------------------------------------

    def on_btnBajasHabitacion_clicked(self,widget):
        try:
            numero = variables.filahab[0].get_text()

            if numero != '':
                funcionesHab.bajaHab(numero)
                funcionesReservas.listadonumhab(self)
            else:
                print("numero inexistente")
        except Exception as e:
            print('Error baja habitacion',e)

    # ---------------------------------------------------------------


    def on_btnModificarHabitacion_clicked(self,widget):
        try:
            numero = variables.filahab[0].get_text()
            precio = variables.filahab[1].get_text()

            if variables.filarbt[0].get_active() == True:
                tipo = 'Simple'
            elif variables.filarbt[1].get_active() == True:
                tipo = 'Double'
            elif variables.filarbt[2].get_active() == True:
                tipo = 'Familiar'

            registro = (numero,tipo,precio)

            if numero != '' and precio != '':
                funcionesHab.modificarHab(registro)
                funcionesHab.listadohab(variables.listhabitaciones)
                funcionesHab.clearEntry(variables.filahab)

        except Exception as e:
            print("Error modificar habitacion",e)

    # ---------------------------------------------------------------

    def on_TreeHabitaciones_cursor_changed(self,widget):
        try:
            model,iter = variables.treehabitaciones.get_selection().get_selected()

            funcionesHab.clearEntry(variables.filahab)

            if iter is not None:
                snumhab = model.get_value(iter,0)
                stipo = model.get_value(iter,1)
                sprecio = model.get_value(iter,2)
                sprecio = round(sprecio,2)

                variables.filahab[0].set_text(str(snumhab))
                variables.filahab[1].set_text(str(sprecio))

                if stipo == 'Simple':
                    variables.filarbt[0].set_active(True)
                elif stipo == 'Double':
                    variables.filarbt[1].set_active(True)
                elif stipo == 'Familiar':
                    variables.filarbt[2].set_active(True)

        except Exception as e:
            print(e)
    # ---------------------------------------------------------------


    # Eventos de la TOOLBAR

    def on_btnCliTool_clicked (self,widget):
        try:

            panelactual = variables.panel.get_current_page()

            if panelactual != 0:
                variables.panel.set_current_page(0)
            else:
                pass

        except Exception as e:
            print("Error btnClienteToolBar",e)

    # ---------------------------------------------------------------


    def on_btnReservas_clicked(self,widget):

        try:

            panelactual = variables.panel.get_current_page()

            if panelactual != 1:
                variables.panel.set_current_page(1)
            else:
                pass
        except Exception as e:
            print('Error btnReservasToolBar',e)

    # ---------------------------------------------------------------


    def on_btnHabitacionTB_clicked(self,widget):

        try:

            panelactual = variables.panel.get_current_page()

            if panelactual != 2:
                variables.panel.set_current_page(2)
            else:
                pass
        except Exception as e:
            print('Error btnHabitacionToolBar',e)

    def on_btnServiTool_clicked(self, widget):

        try:
            panelactual = variables.panel.get_current_page()

            if panelactual != 3:
                variables.panel.set_current_page(3)
            else:
                pass
        except Exception as e:
            print('Error btnServiciosToolBar ', e)



    # ---------------------------------------------------------------

    def on_btnLimpiar_clicked(self,widget):

        try:

            funcionesCli.clearEntry(variables.filacli)
            funcionesHab.clearEntry(variables.filahab)
            funcionesReservas.clearEntry(variables.filareserva)

        except Exception as e:
            print('Error btnLimpiar',e)

    # ---------------------------------------------------------------


    def on_btnCalc_clicked (self,widget):

        call('gnome-calculator')

    # ---------------------------------------------------------------

    # Eventos MENU BAR

    def menuBarSalir_activate (self,widget):
        self.salir()

    # ---------------------------------------------------------------

    # Eventos Acerca De

    def on_btnSalirAcercaDe_clicked(self,widget):
       try:
            variables.venacercade.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venacercade.hide()
       except Exception as e:
           print("Error boton salir acerca de : ",e)

    # ---------------------------------------------------------------


    def on_menuBarAcercaDe_activate(self,widget):

        try:
            variables.venacercade.show()
        except Exception as e:
            print("Error boton abrir acerca de : ", e)

    # ---------------------------------------------------------------


    def on_menuBarBackup_activate(self,widget):

        try:
            variables.venfile.show()
        except Exception as e:
            print("Error boton abrir acerca de : ", e)

    # ---------------------------------------------------------------


    def on_btnSalirBackup_clicked(self,widget):
        try:
            variables.venfile.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venfile.hide()
        except Exception as e:
            print("Error boton salir acerca de : ", e)

    # ---------------------------------------------------------------

    # Eventos Backup

    def on_btBackup_clicked(self,widget):
       try:
            conexion.Conexion.cerrarBBDD(self)
            variables.venfiledialog.show()
            conexion.Conexion.abrirBBDD(self)
       except Exception as e:
           print("Error, dialog",e)

    # ---------------------------------------------------------------

    def on_btnAceptarDialog_clicked(self,widget):
        try:

            ruta = os.path.abspath(str(variables.venfiledialog.get_filename()))

            fecha = datetime.datetime.now()

            compression = zipfile.ZIP_DEFLATED

            fichero = '/media/DIURNO/DI/Empresa/venv/empresa.sqlite'

            name = str(fecha) + "_copia.zip"

            backup = zipfile.ZipFile(name, mode = 'w')

            backup.write(fichero, compress_type = compression)

            shutil.move(name, ruta)

            variables.venfiledialog.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venfiledialog.hide()

            variables.lblmensajedialog.set_text("Copia creada con éxito");
            variables.vendialogcorrecto.show()

        except Exception as e:
            variables.venfiledialog.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venfiledialog.hide()

            variables.lblmensajedialog.set_text("Error durante la copia");
            variables.vendialogcorrecto.show()
            print(e)

    # ---------------------------------------------------------------

    def on_btnCancelarDialog_clicked(self,widget):
        variables.venfiledialog.connect('delete-event', lambda w, e: w.hide() or True)
        variables.venfiledialog.hide()

    # ---------------------------------------------------------------

    def on_btnAceptarRdy_clicked(self,widget):
        variables.vendialogcorrecto.connect('delete-event', lambda w, e: w.hide() or True)
        variables.vendialogcorrecto.hide()

    # ---------------------------------------------------------------


# RESERVAS

    def on_btnCheckIn_clicked(self,widget):
        try:
            variables.vencalendarr1.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendarr1.show()
            variables.semaforo = 2
        except Exception as e:
            print("Error abrir calendario", e)

    # ---------------------------------------------------------------

    def on_btnCheckOut_clicked(self,widget):
        try:
            variables.vencalendarr2.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendarr2.show()
            variables.semaforo = 3
        except Exception as e:
            print("Error abrir calendario", e)

    # ---------------------------------------------------------------

    def on_btnAltasReservas_clicked(self,widget):
        try:

            dni = variables.filareserva[0].get_text()
            apel = variables.filareserva[1].get_text()
            habitacion = variables.numhab
            fecha1 = variables.filareserva[2].get_text()
            fecha2 = variables.filareserva[3].get_text()
            numnoches = variables.filareserva[4].get_text()
            registro = (dni, apel, habitacion, fecha1, fecha2, numnoches)

            if dni != '' and apel != '' and fecha1 != '' and fecha2 != '':

                entrada = datetime.strptime(fecha1, '%d/%m/%Y')
                salida = datetime.strptime(fecha2, '%d/%m/%Y')

                if salida < entrada:
                    pass
                else:
                    comprobar_fechas = False

                    comprobar_existe = funcionesReservas.comprobar_existe(dni, habitacion, fecha1, fecha2)
                    comprobar_fechas = funcionesReservas.comprobarFechas(habitacion, fecha1, fecha2)

                    if len(comprobar_existe) == 0:
                        if comprobar_fechas:
                            funcionesReservas.insertarReservas(registro)
                            funcionesReservas.listadoreservas(variables.listreservas)
                        else:
                            variables.lblmensajedialog.set_text("Error en fecha");
                            variables.vendialogcorrecto.show()

        except Exception as e:
            print("Error alta reserva", e)

    # ---------------------------------------------------------------


    def on_btnBajasReservas_clicked(self,widget):
        try:
            dni = variables.filareserva[0].get_text()
            fecha = variables.filareserva[2].get_text()

            if dni != '':
                funcionesReservas.bajasReservas(dni,fecha)
            else:
                print("dni inexistente")
        except:
            print('Error baja Reserva')

    # ---------------------------------------------------------------

    def on_btnModificarReservas_clicked(self,widget):
        try:

            registro = None

            dni = variables.filareserva[0].get_text()
            apel = variables.filareserva[1].get_text()
            habitacion = variables.numhab
            fecha1 = variables.filareserva[2].get_text()
            fecha2 = variables.filareserva[3].get_text()
            numnoches = variables.filareserva[4].get_text()

            if variables.saveDni != '':
                registro = (dni, apel, habitacion, fecha1, fecha2, numnoches, variables.saveDni)

            if registro is not None:

                funcionesReservas.modificarReserva(registro)
                funcionesReservas.listadoreservas(variables.listreservas)
                funcionesReservas.clearEntry(variables.filareserva)



        except Exception as e:
            print("Error modificar Reserva", e)

    # ---------------------------------------------------------------

    def on_cmbReservasHabitacion_changed(self,widget):
        try:

            index = variables.cmbreserhabitacion.get_active()
            model = variables.cmbreserhabitacion.get_model()
            item = model[index]
            variables.numhab = item[0]


        except Exception as e:
            print("Error evento comboBox",e)

    # ---------------------------------------------------------------

    def on_treeReservas_cursor_changed(self, widget):
        try:

            model, iter = variables.treereservas.get_selection().get_selected()

            if iter is not None:
                dni = model.get_value(iter,0)
                apellidos = model.get_value(iter,1)
                checkin = model.get_value(iter,3)
                checkout = model.get_value(iter,4)
                noches = model.get_value(iter,5)
                habitacion = model.get_value(iter,2)
                funcionesReservas.buscarHabitacion(habitacion)

                variables.filareserva[0].set_text(str(dni))
                variables.saveDni = dni
                variables.filareserva[1].set_text(str(apellidos))
                variables.filareserva[2].set_text(str(checkin))
                variables.filareserva[3].set_text(str(checkout))
                variables.filareserva[4].set_text(str(noches))

                variables.lbldnifacturacion.set_text(str(dni))
                variables.lblapellidosfacturacion.set_text(str(funcionesCli.findApellidos(dni)))
                variables.lblnombrefacturacion.set_text(str(funcionesCli.findNombre(dni))) # Poner método que busque el nombre del cliente
                variables.lblcodigoreserva.set_text(str(funcionesReservas.findID(dni,habitacion))) # Poner método que busque el codigo de la reserva
                variables.lblhabitacionfacturacion.set_text(str(habitacion))
                variables.lblfechafacturacion.set_text(str(checkout))

                variables.filafacturacion[0].set_text(variables.lblnochesfac.get_text())
                variables.filafacturacion[1].set_text(str(noches))
                variables.filafacturacion[2].set_text(str(funcionesHab.findPrecio(habitacion))) #Metodo que devuelva el precio de la habitacion
                variables.filafacturacion[3].set_text(str(funcionesHab.precioTotal(noches,funcionesHab.findPrecio(habitacion)))) #Método que calcule el total a pagar

                variables.datosfactura = (variables.lblcodigoreserva, variables.lblfechafacturacion, variables.lbldnifacturacion,
                                          variables.lblhabitacionfacturacion, variables.lblapellidosfacturacion, variables.lblnombrefacturacion)

                # Cargar datos en el apartado servicios
                variables.lblreservaservicio.set_text(str(variables.lblcodigoreserva.get_text()))
                variables.lblhabitacionservicio.set_text(str(habitacion))

                funcionesServicios.listadoservicios(variables.listservicios, variables.lblcodigoreserva.get_text())
                funcionesServicios.imprimirservicioprecio(variables.lblcodigoreserva.get_text())
                funcionesServicios.calcularPrecioNoIva(variables.preciosconcepto, variables.lblcodigoreserva.get_text())
                funcionesServicios.calcularIva(variables.lblcodigoreserva.get_text())
                funcionesServicios.calcularTotalPagar()

        except Exception as e:
            print("Error TreeView Reservas ",e)

    # ---------------------------------------------------------------
    
    def on_btnPrintFac_clicked(self, widget):
        try:

            impresion.factura()

        except Exception as e:
            print('Error evento impresion',e)

    # ---------------------------------------------------------------


    # Eventos servicios
    # ---------------------------------------------------------------
    def on_btnServicioBasicoAlta_clicked(self,widget):

        global tipo, precio

        reserva = variables.lblcodigoreserva.get_text()

        registropark = ''
        servicio = ''
        preciopark = ''

        if variables.radiobuttonservicios[0].get_active():
            tipo = ''
            precio = ''
        elif variables.radiobuttonservicios[1].get_active():
            tipo = 'Desayuno'
            precio = 20.85
        else:
            tipo = 'Comida'
            precio = 17.85

        if variables.btncheckparking.get_active():
            servicio = 'Parking'
            preciopark = 30

            registropark = (servicio, preciopark, reserva)

        else:
            servicio = ''
            preciopark = ''

        # -----------------------------------------------------------

        if reserva != '' and tipo != '':

            existencia = funcionesServicios.comprobarexistencia(reserva, tipo)

            if existencia == '':
                registro = (tipo, precio, reserva)
                funcionesServicios.insertarServicios(registro)
                funcionesServicios.listadoservicios(variables.listservicios,reserva)
                funcionesServicios.imprimirservicioprecio(reserva)

            if registropark != '':
                existencia = funcionesServicios.comprobarexistencia(reserva, servicio)

                if existencia == '':
                    funcionesServicios.insertarServicios(registropark)
                    funcionesServicios.listadoservicios(variables.listservicios, reserva)
                    funcionesServicios.imprimirservicioprecio(reserva)

        elif reserva != '' and registropark != '' and tipo == '':

            existencia = funcionesServicios.comprobarexistencia(reserva, servicio)

            if existencia == '':
                funcionesServicios.insertarServicios(registropark)
                funcionesServicios.listadoservicios(variables.listservicios, reserva)
                funcionesServicios.imprimirservicioprecio(reserva)

        funcionesServicios.calcularPrecioNoIva(variables.preciosconcepto, variables.lblcodigoreserva.get_text())
        funcionesServicios.calcularIva(variables.lblcodigoreserva.get_text())
        funcionesServicios.calcularTotalPagar()

    # ---------------------------------------------------------------------------------
    def on_btnServicioAdicionalAlta_clicked(self, widget):

        reserva = variables.lblcodigoreserva.get_text()
        tipo = variables.enttiposervicio.get_text()
        precio = variables.entprecioservicio.get_text()

        if reserva != '' and tipo != '' and precio != '':

            existencia = funcionesServicios.comprobarexistencia(reserva, tipo)

            if existencia == '':
                registro = (tipo, precio, reserva)
                funcionesServicios.insertarServicios(registro)
                funcionesServicios.listadoservicios(variables.listservicios, reserva)
                funcionesServicios.imprimirservicioprecio(reserva)
                variables.enttiposervicio.set_text('')
                variables.entprecioservicio.set_text('')

            else:
                pass

        funcionesServicios.calcularPrecioNoIva(variables.preciosconcepto, variables.lblcodigoreserva.get_text())
        funcionesServicios.calcularIva(variables.lblcodigoreserva.get_text())
        funcionesServicios.calcularTotalPagar()

    # ---------------------------------------------------------------------------------

    def on_btnEliminarServicio_clicked(self, widget):
        try:

            if variables.codigoservicio != '' and variables.lblreservaservicio.get_text() != '':
                funcionesServicios.borrarServicios(variables.codigoservicio, variables.lblreservaservicio.get_text())
                funcionesServicios.imprimirservicioprecio(variables.lblreservaservicio.get_text())
                variables.codigoservicio = ''
                funcionesServicios.calcularPrecioNoIva(variables.preciosconcepto, variables.lblcodigoreserva.get_text())
                funcionesServicios.calcularIva(variables.lblcodigoreserva.get_text())
                funcionesServicios.calcularTotalPagar()
            else:
                print("servicio no seleccionado")
        except Exception as e:
            print('Error baja Servicio', e)

    # ---------------------------------------------------------------------------------

    def on_treeServicios_cursor_changed(self,widget):
        try:
            model,iter = variables.treeservicios.get_selection().get_selected()

            if iter is not None:
                codigoservicio = model.get_value(iter,0)
                stipo = model.get_value(iter,1)

                variables.codigoservicio = str(codigoservicio)

                if stipo == 'Desayuno':
                    variables.filarbt[1].set_active(True)
                elif stipo == 'Comida':
                    variables.filarbt[2].set_active(True)
                else:
                    variables.filarbt[0].set_active(True)

        except Exception as e:
            print(e)

    '''
        BigData Importar y Exportar
    '''
    # Importar
    def on_menuBarImportar_activate(self, widget):


        try:
            fila = None
            # Abrimos el fichero excel
            document = xlrd.open_workbook("listadoclientes.xlsx")

            # Guarda cada una de las hojas y el número indica la hoja
            clientes = document.sheet_by_index(0)

            cont = 0

            for i in range(clientes.nrows):
                if cont != 0:
                    dni = clientes.cell_value(rowx=i, colx=0)
                    apellidos = clientes.cell_value(rowx=i, colx=1)
                    nombre = clientes.cell_value(rowx=i, colx=2)
                    fechatabla = xlrd.xldate_as_datetime(clientes.cell_value(rowx=i, colx=3),document.datemode)
                    fecha = datetime.date(fechatabla)

                    fila = (dni,apellidos,nombre,fecha)

                    if fila is not None:
                        funcionesCli.insertarcli(fila)
                        funcionesCli.listadocli(variables.listclientes)

                else:
                    cont = 1

            variables.lblmensajedialog.set_text("Clientes insertados!");
            variables.vendialogcorrecto.show()
        except Exception as e:
            print("Error posible fallo ", e)

    # Exportar
    def on_btnBarExportar_activate(self, widget):
        style0 = xlwt.easyxf('font: name Times New Roman, colour red, bold on')
        style1 = xlwt.easyxf("", num_format_str='DD-MM-YYYY')

        wb = xlwt.Workbook()

        ws = wb.add_sheet('NuevoClientes', cell_overwrite_ok=True)
        ws.write(0, 0, 'DNI', style0)
        ws.write(0, 1, 'APELLIDOS', style0)
        ws.write(0, 2, 'NOMBRE', style0)
        ws.write(0, 3, 'FECHA ALTA', style0)

        datos = funcionesCli.listar()

        fila = 1
        for registro in datos:
            columna = 0
            cont = 0
            for dato in registro:
                if cont != 0:
                    ws.write(fila, columna, dato, style1)
                    columna = columna + 1
                cont = cont + 1
            fila = fila + 1

        wb.save('ArchivoExportado.xls')

    def on_btnListarClientes_clicked(self, widget):
        impresion.clientes()

    def on_btnImprimir_clicked(self, widget):
        impresion.clientes()