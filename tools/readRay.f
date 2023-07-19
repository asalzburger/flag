*     .................................................................
*     user program or subroutine
*     .................................................................
      PARAMETER (LUNRAY = 10)
      CHARACTER MATNAM*8, FILNAM*80
      INTEGER*8 MLATTC, MLATLD
      INTEGER NRAYRN, MREG, MMAT, MREGLD, MMATLD, IDISC
      REAL EKIN, XX, YY, ZZ, R2, R3, THETAP, PHIPOS, TXX, TYY, TZZ,
     &     THETAD, PHIDIR, ETADIR, RCM, ALAMDI, ALAMDP, ALAMDN, ALAMDG,
     &     ALAMDR, DEKMIP, GMOCM2, DELAGE, RCMTOT, ALITOT, ALPTOT,
     &     ALNTOT, ALGTOT, ALRTOT, TOTMIP, SRHTOT, AGEAGE
*     .................................................................
*     here other possible declarations
*     .................................................................
      !  Ask the user for the name of the file
      !  WRITE (*,*) ' File name?'
      !  READ  (*,'(A80)') FILNAM
      ! Predetermined file name
       FILNAM = "fort.10"
       OPEN (FILE = FILNAM, UNIT = LUNRAY, STATUS = 'OLD', FORM =
     &     'UNFORMATTED')
      write(*,*) "Eta distance X0"

*     loop over several rays
    1 CONTINUE
*     read info about ray starting point
      READ (LUNRAY, END = 3000, ERR=1000) NRAYRN, MREG, MLATTC,
     &                                      MMAT, EKIN
      READ (LUNRAY, END = 1000) XX0, YY0, ZZ0, R2, R3, THETAP, PHIPOS
      READ (LUNRAY, END = 1000) TXX, TYY, TZZ, THETAD, PHIDIR, ETADIR
*       where:
*       NRAYRN = ray number
*       MREG   = starting region
*       MLATTC = starting lattice cell
*       MMAT   = material of starting region
*       EKIN   = reference kinetic energy of the ray (GeV)
*       XX, YY, ZZ = ray starting point
*       R2     = distance of ray starting point from z-axis (cm)
*       R3     = distance of ray starting point from the origin (cm)
*       THETAP = polar angle between the position vector of the ray
*                starting point and the z-axis (radians)
*       PHIPOS = azimuthal angle of the position vector of the ray
*                starting point around the z-axis (radians)
*       TXX, TYY, TZZ = ray direction cosines
*       THETAD = polar angle between the ray and the z-axis (radians)
*       PHIDIR = azimuthal angle of ray around the z-axis (radians)
*       ETADIR = pseudorapidity of ray direction with respect to the
*                direction defined by option BEAMPOS
*       ................................................................
*       here possible user code to manipulate values read
*       ................................................................
*       loop over further positions along the ray path
  2   CONTINUE
*     read info about next point
      READ (LUNRAY, END = 2000) MREGLD, MLATLD, MMATLD,
     &                              MATNAM, IDISC
      READ (LUNRAY, END = 2000) XX, YY, ZZ, R2, R3, THETAP, PHIPOS
      READ (LUNRAY, END = 2000) RCM, ALAMDI, ALAMDP, ALAMDN, ALAMDG,
     &                              ALAMDR, DEKMIP, GMOCM2, DELAGE
      READ (LUNRAY, END = 2000) RCMTOT, ALITOT, ALPTOT, ALNTOT,
     &                              ALGTOT, ALRTOT, TOTMIP, SRHTOT,
     &                              AGEAGE
*         where:
*         MREGLD = number of next region traversed by ray
*         MLATLD = number of next lattice cell traversed by ray
*         MMATLD = material of next region
*         MATNAM = name of material of next region
*         IDISC  = 0 unless next region is blackhole
*         XX, YY, ZZ, R2, R3, THETAP, PHIPOS: as described above, but
*                  referred to the current position
*         RCM    = distance traversed from last point to here
*         ALAMDI = distance traversed from last point to here, in units
*                  of high energy nucleon inelastic mean free paths (at
*                  the reference kinetic energy of the ray)
*         ALAMDP = distance traversed from last point to here, in units
*                  of high energy pion inelastic mean free paths (at the
*                  reference kinetic energy of the ray)
*         ALAMDN = distance traversed from last point to here, in units
*                  of maximum neutron inelastic mean free paths (i.e.,
*                  at 200 MeV)
*         ALAMDG = distance traversed from last point to here, in units
*                  of maximum photon mean free paths (i.e., at so-called
*                  Compton minimum). **Note:** if the EMF option has not
*                  been requested, ALAMDG has always zero value
*         ALAMDR = distance traversed from last point to here, in units
*                  of radiation lengths. **Note:** if the EMF option has not
*                  been requested, ALAMDR is calculated but only in an
*                  approximate way
*         DEKMIP = energy lost from last point to here by a minimum
*                  ionising muon
*         GMOCM2 = distance traversed from last point to here in g/cm2
*         DELAGE = time elapsed from last point to here in sec (i.e.,
*                  distance divided by speed of light)
*         RCMTOT = cumulative distance traversed so far in cm
*         ALITOT = cumulative distance traversed so far, in units of
*                  high energy nucleon inelastic mean free paths
*         ALPTOT = cumulative distance traversed so far, in units of
*                  high energy pion inelastic mean free paths
*         ALNTOT = cumulative distance traversed so far, in units of
*                  maximum neutron inelastic mean free paths
*         ALGTOT = cumulative distance traversed so far, in units of
*                  maximum photon mean free paths (i.e., at so-called
*                  Compton minimum). **Note:** if the EMF option has not
*                  been requested, ALGTOT has always zero value
*         ALRTOT = cumulative distance traversed so far, in units of
*                  radiation lengths. **Note:** if the EMF option has not
*                  been requested, ALRTOT is calculated but only in an
*                  approximate way
*         TOTMIP = cumulative energy lost so far by a minimum ionising
*                  muon
*         SRHTOT = cumulative distance traversed so far in g/cm2
*         AGEAGE = cumulative time elapsed so far in sec
*         .............................................................
*         possible user code to manipulate values read
*         .............................................................
      IF ( IDISC .EQ. 0 ) THEN
*           ...........................................................
*           possible user code at the end of ray step
*           ...........................................................
*        write(*,*) '--->',etadir,xx,yy,zz,mreg,mregld
        GO TO 2
      END IF
*       ...............................................................
*       possible user code at the end of ray trajectory
*       ...............................................................
*       new ray
      write(*,*) etadir,rcmtot,alrtot
      GO TO 1
 1000 CONTINUE
      WRITE(*,*) ' Incomplete data on file about ray starting point'
      GO TO 3000
 2000 CONTINUE
      WRITE(*,*) ' Incomplete data on file about ray trajectory'
 3000 CONTINUE
*     .................................................................
*     possible user code at the end of analysis
*     .................................................................
      CLOSE (UNIT = LUNRAY)
      END
