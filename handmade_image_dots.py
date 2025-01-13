from pathlib import Path
outFields = QgsFields()
outFields.append( QgsField( QStringLiteral( "photo" ), QVariant.String ) );
outFields.append( QgsField( QStringLiteral( "filename" ), QVariant.String ) );
outFields.append( QgsField( QStringLiteral( "directory" ), QVariant.String ) );
outFields.append( QgsField( QStringLiteral( "altitude" ), QVariant.Double ) );
outFields.append( QgsField( QStringLiteral( "direction" ), QVariant.Double ) );
outFields.append( QgsField( QStringLiteral( "rotation" ), QVariant.Int ) );
outFields.append( QgsField( QStringLiteral( "longitude" ), QVariant.String ) );
outFields.append( QgsField( QStringLiteral( "latitude" ), QVariant.String ) );
outFields.append( QgsField( QStringLiteral( "timestamp" ), QVariant.DateTime ) );